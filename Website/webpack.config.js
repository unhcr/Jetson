const CopyWebpackPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const webpack = require('webpack');
const path = require('path');
const process = require('process');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const isDevServer = process.env.WEBPACK_SERVE ? true : false;

module.exports = {
  mode: isDevServer ? 'development' : 'production',
  context: path.resolve(__dirname, './src'),
  entry: {
    index: './index.js',
    terms: './terms.js'
  },
  optimization: {
    splitChunks: {
      cacheGroups: {
        commons: {
          name: 'commons',
          chunks: 'initial',
          minChunks: 2,
          minSize: 0
        }
      }
    },
    occurrenceOrder: true, // To keep filename consistent between different modes (for example building only)
    minimizer: [
      new UglifyJsPlugin({
        cache: true,
        parallel: true,
        sourceMap: true
      }),
      new OptimizeCSSAssetsPlugin({})
    ]
  },
  output: {
    path: path.resolve(__dirname, 'dist')
    // filename: 'bundle.js'
  },
  devtool: 'source-map',
  plugins: [
    new webpack.ProvidePlugin({
      jQuery: 'jquery'
    }),
    new CopyWebpackPlugin([
      { from: '*.html' },
      { from: 'favicon.ico' },
      { from: 'img/*' },
      { from: 'fonts/*' },
      { from: 'json/*' }
    ]),
    new MiniCssExtractPlugin({
      filename: 'bundle.css'
    })
  ],
  module: {
    rules: [
      {
        test: /\.(sa|sc|c)ss/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'postcss-loader',
          'sass-loader'
        ]
      },
      {
        test: /\.(woff|woff2|ttf|eot|svg)$/,
        loader: 'url-loader?limit=100000'
      },
      {
        test: /\.js$/,
        use: {
          loader: 'babel-loader',
          options: {
            exclude: isDevServer ? /node_modules/ : undefined,
            presets: ['@babel/preset-env'],
            cacheDirectory: true
          }
        }
      }
    ]
  }
};
