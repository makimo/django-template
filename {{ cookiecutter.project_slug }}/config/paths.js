const path = require('path');

const baseDir       = path.resolve();
const baseOutputDir = path.join(baseDir, '{{ cookiecutter.project_slug }}', 'static');
const baseInputDir  = path.join(baseDir, '{{ cookiecutter.project_slug }}', 'assets');

module.exports = {
    baseDir:        baseDir,
    baseOutputDir:  baseOutputDir,
    baseInputDir:   baseInputDir,
    localOutputDir: path.join(baseOutputDir, 'local'),
    distOutputDir:  path.join(baseOutputDir, 'dist')
}
