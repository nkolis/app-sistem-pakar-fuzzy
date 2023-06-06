const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
module.exports = {
  entry: './main.js',
  mode: 'development',
  plugins: [
    // Plugin untuk memisahkan file CSS
    new MiniCssExtractPlugin({
      filename: 'styles.css',
    }),
    new CssMinimizerPlugin(),

  ],

  output: {
    path: path.resolve(__dirname, 'static/dist'),
    filename: 'main.js',
  },
  devServer: {
    static: {
      directory: path.resolve(__dirname, 'templates'),
    },
    port: 3000,
    open: true,
    hot: true,
    compress: true,
    historyApiFallback: true,
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-react'],
          },
        },
      },
      {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, 'css-loader', 'postcss-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.css'],
  },
};
