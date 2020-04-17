const paths         = require('./paths.js');

const path          = require('path');
const webpack       = require('webpack');
const webpackMerge  = require('webpack-merge');
const baseConfig    = require('./webpack.base.js');
const WebpackAssetsManifest = require('webpack-assets-manifest');


module.exports = webpackMerge(baseConfig, {
    output: {
        path: path.resolve(__dirname, paths.distOutputDir),
        filename: '[name].[chunkhash].js'
    },
    plugins: [
        new WebpackAssetsManifest({
            output: path.resolve() + '/webpack-stats.dist.json'
        })
    ]
});
