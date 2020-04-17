const paths         = require('./paths.js');

const path          = require('path');
const webpackMerge  = require('webpack-merge');
const baseConfig    = require('./webpack.base.js');
const WebpackAssetsManifest = require('webpack-assets-manifest');


module.exports = webpackMerge(baseConfig, {
    output: {
        path: path.resolve(__dirname, paths.localOutputDir),
        filename: '[name].[chunkhash].js'
    },
    plugins: [
        new WebpackAssetsManifest({
            output: path.resolve() + '/webpack-stats.local.json'
        })
    ]
});
