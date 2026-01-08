import { defineConfig } from '@rsbuild/core';
import HtmlRspackPlugin from 'html-rspack-plugin';
import { pluginVue2 } from '@rsbuild/plugin-vue2';
import { pluginSass } from '@rsbuild/plugin-sass';

export default defineConfig({
  plugins: [pluginVue2(), pluginSass()],

  source: {
    entry: {
      app: './{{ cookiecutter.project_slug }}/assets/app.js',
      hello_world_mount: './{{ cookiecutter.project_slug }}/assets/components/hello_world_mount.js',
    },
  },

  output: {
    distPath: {
      root: '{{ cookiecutter.project_slug }}/static/local',
      js: '.',
      css: '.',
      svg: 'assets/images',
      font: 'assets/fonts',
      image: 'assets/images',
      media: 'assets/images',
    },
    filename: {
      js: '[name].[contenthash].js',
      css: '[name].[contenthash].css',
    },
    assetPrefix: '/static/',
    cleanDistPath: true,
  },

  tools: {
    rspack: (config, { environment }) => {
      // Disable HTML plugin completely
      config.plugins = config.plugins.filter(
        plugin => plugin.constructor.name !== 'HtmlRspackPlugin'
      );

      // Generate separate JS and CSS tag files for each entry point
      const entryPoints = ['app', 'hello_world_mount'];

      entryPoints.forEach(entryName => {
        config.plugins.push(
          new HtmlRspackPlugin({
            inject: false,
            filename: `${entryName}-css-tags.html`,
            chunks: [entryName],
            templateContent: ({ htmlWebpackPlugin }) => {
              const { css = [] } = htmlWebpackPlugin.files;
              return css.map(href => `<link rel="stylesheet" href="${href}">`).join('\n');
            },
          })
        );

        config.plugins.push(
          new HtmlRspackPlugin({
            inject: false,
            filename: `${entryName}-js-tags.html`,
            chunks: [entryName],
            templateContent: ({ htmlWebpackPlugin }) => {
              const { js = [] } = htmlWebpackPlugin.files;
              return js.map(src => `<script defer src="${src}"></script>`).join('\n');
            },
          })
        );
      });

      return config;
    },
  },

  environments: {
    local: {
      output: {
        distPath: {
          root: '{{ cookiecutter.project_slug }}/static/local',
        },
      },
    },
    dist: {
      output: {
        distPath: {
          root: '{{ cookiecutter.project_slug }}/static/dist',
        },
      },
    },
  },
});
