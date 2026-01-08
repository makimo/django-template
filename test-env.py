#!/usr/bin/env python3
"""
Test script for django-template cookiecutter.

Generates a project, starts Docker services, runs validation checks,
and cleans up all artifacts.
"""

import argparse
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

# Exit codes
EXIT_SUCCESS = 0
EXIT_PREREQ_FAILED = 1
EXIT_COOKIECUTTER_FAILED = 2
EXIT_DOCKER_BUILD_FAILED = 3
EXIT_DOCKER_START_FAILED = 4
EXIT_VALIDATION_FAILED = 5

# Default values
# Use the directory where this script is located as the template directory
SCRIPT_DIR = Path(__file__).parent.resolve()
DEFAULT_TEMPLATE_DIR = str(SCRIPT_DIR)

# Global state for signal handler
_cleanup_state = {
    'project_path': None,
    'project_slug': None,
    'compose_dir': None,
    'verbose': False,
    'foreground': False,
}
DEFAULT_TIMEOUT = 1 * 60 # 1 minute
DEFAULT_LICENSE = 'Proprietary'


def sigint_handler(signum, frame):
    """Handle Ctrl+C during foreground mode."""
    print("\n\nInterrupted by user (Ctrl+C)")

    if _cleanup_state['foreground'] and _cleanup_state['compose_dir']:
        print("Stopping Docker containers...")
        try:
            subprocess.run(
                ['docker', 'compose', 'down', '--volumes', '--remove-orphans'],
                cwd=_cleanup_state['compose_dir'],
                capture_output=True,
                timeout=60,
            )
            print("Docker containers stopped.")
        except Exception as e:
            print(f"Warning: Failed to stop containers: {e}")

        # Clean up db directory
        db_dir = _cleanup_state['compose_dir'] / 'db'
        if db_dir.exists():
            try:
                shutil.rmtree(db_dir)
            except Exception:
                pass

    if _cleanup_state['project_path'] and _cleanup_state['project_path'].exists():
        print(f"Removing project directory: {_cleanup_state['project_path']}")
        try:
            shutil.rmtree(_cleanup_state['project_path'])
            print("Project directory removed.")
        except Exception as e:
            print(f"Warning: Failed to remove directory: {e}")

    sys.exit(130)


class CreateEnvError(Exception):
    """Base exception for create-env errors."""
    exit_code = 1


class PrerequisiteError(CreateEnvError):
    exit_code = EXIT_PREREQ_FAILED


class CookiecutterError(CreateEnvError):
    exit_code = EXIT_COOKIECUTTER_FAILED


class DockerBuildError(CreateEnvError):
    exit_code = EXIT_DOCKER_BUILD_FAILED


class DockerStartupError(CreateEnvError):
    exit_code = EXIT_DOCKER_START_FAILED


class ValidationError(CreateEnvError):
    exit_code = EXIT_VALIDATION_FAILED


def print_step(message):
    """Print a step header."""
    print(f"\n{'=' * 60}")
    print(f"  {message}")
    print(f"{'=' * 60}\n")


def print_check(message, success=True):
    """Print a check result."""
    status = "[OK]" if success else "[FAIL]"
    print(f"  {status} {message}")


def run_command(cmd, timeout=60, capture=True, cwd=None, ignore_errors=False, verbose=False):
    """Run a command with timeout and optional error handling."""
    if verbose:
        print(f"  Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=timeout,
            cwd=cwd,
        )

        if result.returncode != 0 and not ignore_errors:
            stderr = result.stderr if capture else ""
            raise subprocess.CalledProcessError(
                result.returncode, cmd, result.stdout, stderr
            )

        return result
    except subprocess.TimeoutExpired as e:
        if not ignore_errors:
            raise
        return None
    except FileNotFoundError:
        if not ignore_errors:
            raise
        return None


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Test django-template cookiecutter by generating a project, '
                    'starting Docker services, and running validation checks.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exit codes:
  0  Success - all checks passed
  1  Prerequisites check failed
  2  Cookiecutter generation failed
  3  Docker build failed
  4  Docker startup failed
  5  Validation checks failed

Examples:
  %(prog)s "My Test Project"
  %(prog)s "Test" --no-remove
  %(prog)s "Test" --template-dir /path/to/django-template
  %(prog)s "Test" --timeout 600 -v
'''
    )

    parser.add_argument(
        'project_name',
        help='Name of the test project (e.g., "Test Project")'
    )
    parser.add_argument(
        '--no-remove',
        action='store_true',
        help='Keep the generated directory after testing'
    )
    parser.add_argument(
        '--keep-docker',
        action='store_true',
        help='Keep Docker containers running for inspection (implies --no-remove)'
    )
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Just clean up existing project directory and exit'
    )
    parser.add_argument(
        '-f', '--foreground',
        action='store_true',
        help='Run Docker in foreground mode (for manual testing)'
    )
    parser.add_argument(
        '--template-dir',
        default=DEFAULT_TEMPLATE_DIR,
        help=f'Path to django-template (default: {DEFAULT_TEMPLATE_DIR})'
    )
    parser.add_argument(
        '--output-dir',
        default='.',
        help='Directory to create project in (default: current directory)'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f'Timeout for docker operations in seconds (default: {DEFAULT_TIMEOUT})'
    )
    parser.add_argument(
        '--license',
        choices=['Proprietary', 'MIT'],
        default=DEFAULT_LICENSE,
        help=f'License choice for cookiecutter (default: {DEFAULT_LICENSE})'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    return parser.parse_args()


def check_prerequisites(args):
    """Phase 1: Verify all requirements are met."""
    print_step("Phase 1: Checking prerequisites")

    # Check Python version
    if sys.version_info < (3, 8):
        raise PrerequisiteError(
            f"Python 3.8+ required, got {sys.version_info.major}.{sys.version_info.minor}"
        )
    print_check(f"Python {sys.version_info.major}.{sys.version_info.minor}")

    # Check cookiecutter
    try:
        result = run_command(['cookiecutter', '--version'], verbose=args.verbose)
        version = result.stdout.strip() if result.stdout else "installed"
        print_check(f"cookiecutter {version}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise PrerequisiteError(
            "cookiecutter not found. Install with: pip install cookiecutter"
        )

    # Check Docker daemon
    try:
        run_command(['docker', 'info'], verbose=args.verbose)
        print_check("Docker daemon running")
    except subprocess.CalledProcessError:
        raise PrerequisiteError(
            "Docker daemon not running. Please start Docker."
        )
    except FileNotFoundError:
        raise PrerequisiteError(
            "Docker not found. Please install Docker."
        )

    # Check docker compose
    try:
        result = run_command(['docker', 'compose', 'version'], verbose=args.verbose)
        version = result.stdout.strip() if result.stdout else "installed"
        print_check(f"docker compose {version}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise PrerequisiteError(
            "docker compose not found. Please ensure Docker Compose V2 is installed."
        )

    # Check template directory
    template_dir = Path(args.template_dir).resolve()
    if not template_dir.exists():
        raise PrerequisiteError(
            f"Template directory not found: {template_dir}"
        )

    cookiecutter_json = template_dir / 'cookiecutter.json'
    if not cookiecutter_json.exists():
        raise PrerequisiteError(
            f"Not a cookiecutter template: {template_dir} (missing cookiecutter.json)"
        )
    print_check(f"Template directory: {template_dir}")

    # Check output directory
    output_dir = Path(args.output_dir).resolve()
    if not output_dir.exists():
        raise PrerequisiteError(
            f"Output directory not found: {output_dir}"
        )
    if not os.access(output_dir, os.W_OK):
        raise PrerequisiteError(
            f"Output directory not writable: {output_dir}"
        )
    print_check(f"Output directory: {output_dir}")

    return template_dir, output_dir


def cleanup_existing_project(project_path, project_slug, verbose):
    """Clean up an existing project directory."""
    if not project_path.exists():
        return

    print(f"  Cleaning up existing project at: {project_path}")

    compose_dir = project_path / 'docker' / 'development'
    if compose_dir.exists():
        cleanup_docker(compose_dir, project_slug, verbose)

    print(f"  Removing project directory: {project_path}")
    try:
        shutil.rmtree(project_path)
        print_check("Existing project removed")
    except Exception as e:
        raise CookiecutterError(f"Failed to remove existing project: {e}")


def generate_project(args, template_dir, output_dir):
    """Phase 2: Run cookiecutter to generate the project."""
    print_step("Phase 2: Generating project from template")

    project_slug = args.project_name.lower().replace(' ', '_')
    project_path = output_dir / project_slug

    # Clean up if project already exists
    if project_path.exists():
        cleanup_existing_project(project_path, project_slug, args.verbose)

    print(f"  Project name: {args.project_name}")
    print(f"  Project slug: {project_slug}")
    print(f"  Output path: {project_path}")
    print()

    # Run cookiecutter
    cmd = [
        'cookiecutter',
        str(template_dir),
        '--no-input',
        f'project_name={args.project_name}',
        f'license={args.license}',
        '-o', str(output_dir),
    ]

    try:
        run_command(cmd, timeout=120, verbose=args.verbose)
        print_check("Project generated successfully")
    except subprocess.CalledProcessError as e:
        raise CookiecutterError(
            f"Cookiecutter failed: {e.stderr or e.stdout or str(e)}"
        )

    if not project_path.exists():
        raise CookiecutterError(
            f"Project directory was not created: {project_path}"
        )

    return project_path, project_slug


def start_docker_services(project_path, project_slug, timeout, verbose, foreground=False):
    """Phase 3: Pull images and start Docker containers."""
    print_step("Phase 3: Starting Docker services")

    compose_dir = project_path / 'docker' / 'development'
    compose_file = compose_dir / 'docker-compose.yml'

    if not compose_file.exists():
        raise DockerBuildError(
            f"docker-compose.yml not found: {compose_file}"
        )

    # Update global state for signal handler
    _cleanup_state['compose_dir'] = compose_dir
    _cleanup_state['foreground'] = foreground

    # Pull images
    print("  Pulling Docker images...")
    try:
        run_command(
            ['docker', 'compose', 'pull'],
            timeout=timeout,
            cwd=compose_dir,
            verbose=verbose,
        )
        print_check("Docker images pulled")
    except subprocess.CalledProcessError as e:
        raise DockerBuildError(
            f"Docker pull failed: {e.stderr or str(e)}"
        )
    except subprocess.TimeoutExpired:
        raise DockerBuildError(
            f"Docker pull timed out after {timeout} seconds"
        )

    # Start services
    if foreground:
        print("  Starting Docker services in foreground mode...")
        print("  Press Ctrl+C to stop and clean up.\n")
        try:
            # Run in foreground - this will block until Ctrl+C
            subprocess.run(
                ['docker', 'compose', 'up'],
                cwd=compose_dir,
            )
            # If we get here, docker compose exited normally
            return compose_dir, None, None
        except KeyboardInterrupt:
            # Signal handler will take care of cleanup
            raise
    else:
        print("  Starting Docker services...")
        try:
            run_command(
                ['docker', 'compose', 'up', '-d'],
                timeout=60,
                cwd=compose_dir,
                verbose=verbose,
            )
            print_check("Docker services started")
        except subprocess.CalledProcessError as e:
            raise DockerStartupError(
                f"Docker startup failed: {e.stderr or str(e)}"
            )

    # Docker Compose V2 names containers as: <project>-<service>-<n>
    # Project defaults to directory name ("development")
    compose_project = "development"
    db_service = f"{project_slug}-db"
    backend_service = f"{project_slug}-backend"
    frontend_service = f"{project_slug}-frontend"

    db_container = f"{compose_project}-{db_service}-1"
    backend_container = f"{compose_project}-{backend_service}-1"
    frontend_container = f"{compose_project}-{frontend_service}-1"

    print("  Waiting for containers to be running...")
    wait_for_container_running(db_container, timeout, verbose)
    print_check(f"Container {db_container} is running")

    wait_for_container_running(backend_container, timeout, verbose)
    print_check(f"Container {backend_container} is running")

    wait_for_container_running(frontend_container, timeout, verbose)
    print_check(f"Container {frontend_container} is running")

    # Wait for database to be ready
    print("  Waiting for database to be ready...")
    wait_for_database_ready(db_container, project_slug, timeout, verbose)
    print_check("Database is ready")

    return compose_dir, db_container, backend_container


def wait_for_container_running(container_name, timeout, verbose):
    """Wait for a container to be in running state."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        result = run_command(
            ['docker', 'ps', '--filter', f'name={container_name}', '--format', '{{.Status}}'],
            ignore_errors=True,
            verbose=verbose,
        )

        if result and result.stdout:
            status = result.stdout.strip().lower()
            if 'up' in status:
                return True

        time.sleep(2)

    raise DockerStartupError(
        f"Container {container_name} did not start within {timeout} seconds"
    )


def wait_for_database_ready(container_name, project_slug, timeout, verbose):
    """Wait for PostgreSQL to be ready to accept connections."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        result = run_command(
            ['docker', 'exec', container_name, 'pg_isready', '-U', project_slug],
            ignore_errors=True,
            verbose=verbose,
        )

        if result and result.returncode == 0:
            return True

        time.sleep(2)

    raise DockerStartupError(
        f"Database did not become ready within {timeout} seconds"
    )


def run_validation_checks(project_path, project_slug, backend_container, timeout, verbose):
    """Phase 4: Run all validation checks."""
    print_step("Phase 4: Running validation checks")

    # Check file structure
    print("  Checking file structure...")
    check_file_structure(project_path, project_slug)
    print_check("File structure is correct")

    # Check template substitution
    print("  Checking template variable substitution...")
    check_template_substitution(project_path, project_slug)
    print_check("Template variables substituted correctly")

    # Wait for Django to be ready and run Django check
    print("  Waiting for Django application to be ready...")
    wait_for_django_ready(backend_container, timeout, verbose)
    print_check("Django application is ready")

    print("  Running Django system check...")
    check_django_application(backend_container, timeout, verbose)
    print_check("Django system check passed")


def check_file_structure(project_path, project_slug):
    """Verify all expected files were generated."""
    required_files = [
        'manage.py',
        'docker/development/docker-compose.yml',
        'docker/development/scripts/run-development.sh',
        'docker/development/scripts/run-frontend.sh',
        f'{project_slug}/settings/base.py',
        f'{project_slug}/settings/local.py',
        f'{project_slug}/urls.py',
        f'{project_slug}/wsgi.py',
        'package.json',
        'requirements/local.txt',
    ]

    missing = []
    for file in required_files:
        path = project_path / file
        if not path.exists():
            missing.append(file)

    if missing:
        raise ValidationError(
            f"Missing required files: {', '.join(missing)}"
        )


def check_template_substitution(project_path, project_slug):
    """Verify cookiecutter variables were properly substituted."""
    files_to_check = [
        'manage.py',
        f'{project_slug}/settings/base.py',
        'docker/development/docker-compose.yml',
        'package.json',
    ]

    pattern = re.compile(r'\{\{\s*cookiecutter\.')

    for file in files_to_check:
        path = project_path / file
        if path.exists():
            content = path.read_text()
            if pattern.search(content):
                raise ValidationError(
                    f"Unsubstituted template variable found in: {file}"
                )


def wait_for_django_ready(container_name, timeout, verbose):
    """Wait for Django to be ready (migrations complete, server starting)."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        # Check if manage.py exists and is accessible
        result = run_command(
            ['docker', 'exec', container_name, 'python', 'manage.py', 'check', '--deploy'],
            ignore_errors=True,
            verbose=verbose,
        )

        if result and result.returncode == 0:
            return True

        # Also check if container is still running
        ps_result = run_command(
            ['docker', 'ps', '--filter', f'name={container_name}', '--format', '{{.Status}}'],
            ignore_errors=True,
            verbose=verbose,
        )

        if not ps_result or not ps_result.stdout or 'up' not in ps_result.stdout.lower():
            raise ValidationError(
                f"Container {container_name} stopped unexpectedly"
            )

        time.sleep(5)

    raise ValidationError(
        f"Django did not become ready within {timeout} seconds"
    )


def check_django_application(container_name, timeout, verbose):
    """Run Django system checks."""
    result = run_command(
        ['docker', 'exec', container_name, 'python', 'manage.py', 'check'],
        timeout=timeout,
        ignore_errors=True,
        verbose=verbose,
    )

    if not result or result.returncode != 0:
        error_msg = result.stderr if result else "Unknown error"
        raise ValidationError(
            f"Django check failed: {error_msg}"
        )


def cleanup_docker(compose_dir, project_slug, verbose):
    """Remove all Docker artifacts."""
    print("  Stopping and removing Docker containers...")

    # Stop and remove containers, networks, volumes
    run_command(
        ['docker', 'compose', 'down', '--volumes', '--remove-orphans'],
        cwd=compose_dir,
        ignore_errors=True,
        timeout=120,
        verbose=verbose,
    )

    # Remove local db directory created by docker compose
    db_dir = compose_dir / 'db'
    if db_dir.exists():
        print(f"  Removing database directory: {db_dir}")
        try:
            shutil.rmtree(db_dir)
        except Exception as e:
            print(f"  [WARN] Failed to remove db directory: {e}")

    # Clean up dangling images
    run_command(
        ['docker', 'image', 'prune', '-f'],
        ignore_errors=True,
        verbose=verbose,
    )

    print_check("Docker cleanup completed")


def cleanup(project_path, project_slug, remove_directory, keep_docker, verbose):
    """Phase 5: Clean up everything."""
    print_step("Phase 5: Cleaning up")

    compose_dir = project_path / 'docker' / 'development'

    if keep_docker:
        print("  Keeping Docker containers running for inspection")
        print(f"  To clean up manually, run:")
        print(f"    cd {compose_dir} && docker compose down --volumes")
    elif compose_dir.exists():
        cleanup_docker(compose_dir, project_slug, verbose)

    if remove_directory and not keep_docker:
        print(f"  Removing project directory: {project_path}")
        try:
            shutil.rmtree(project_path)
            print_check("Project directory removed")
        except Exception as e:
            print(f"  [WARN] Failed to remove directory: {e}")
    else:
        print(f"  Project directory kept at: {project_path}")


def main():
    args = parse_arguments()
    project_path = None
    project_slug = None

    project_slug = args.project_name.lower().replace(' ', '_')
    output_dir = Path(args.output_dir).resolve()
    project_path = output_dir / project_slug

    # Update global state for signal handler
    _cleanup_state['project_path'] = project_path
    _cleanup_state['project_slug'] = project_slug
    _cleanup_state['verbose'] = args.verbose

    # Handle --clean mode
    if args.clean:
        print(f"\nCleaning up project: {args.project_name}")
        if project_path.exists():
            cleanup_existing_project(project_path, project_slug, args.verbose)
            print("\nCleanup completed successfully.")
        else:
            print(f"\nNo existing project found at: {project_path}")
        return EXIT_SUCCESS

    # Register signal handler for foreground mode
    if args.foreground:
        signal.signal(signal.SIGINT, sigint_handler)
        print(f"\nStarting django-template in foreground mode: {args.project_name}")
    else:
        print(f"\nTesting django-template with project: {args.project_name}")
        print(f"Timeout: {args.timeout} seconds")

    try:
        # Phase 1: Prerequisites
        template_dir, output_dir = check_prerequisites(args)

        # Phase 2: Generate project
        project_path, project_slug = generate_project(args, template_dir, output_dir)

        # Update global state after project is created
        _cleanup_state['project_path'] = project_path

        # Phase 3: Start Docker
        compose_dir, db_container, backend_container = start_docker_services(
            project_path, project_slug, args.timeout, args.verbose,
            foreground=args.foreground
        )

        # In foreground mode, we skip validation (user is manually testing)
        if args.foreground:
            # Docker compose exited normally
            print_step("Docker services stopped.")
            return EXIT_SUCCESS

        # Phase 4: Validation (only in background mode)
        run_validation_checks(
            project_path, project_slug, backend_container,
            args.timeout, args.verbose
        )

        print_step("SUCCESS: All checks passed!")
        return EXIT_SUCCESS

    except CreateEnvError as e:
        print(f"\n[ERROR] {e}")
        return e.exit_code

    except KeyboardInterrupt:
        # In foreground mode, signal handler takes care of cleanup
        if args.foreground:
            return 130
        print("\n\nInterrupted by user")
        return 130

    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        return 1

    finally:
        # Always attempt cleanup (unless foreground mode - signal handler does it)
        if not args.foreground and project_path and project_path.exists():
            try:
                keep_docker = getattr(args, 'keep_docker', False)
                remove_dir = not args.no_remove and not keep_docker
                cleanup(project_path, project_slug, remove_dir, keep_docker, args.verbose)
            except Exception as e:
                print(f"  [WARN] Cleanup failed: {e}")


if __name__ == '__main__':
    sys.exit(main())
