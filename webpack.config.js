const fs = require("fs");
const path = require("path");
const globAll = require("glob-all");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const { PurgeCSSPlugin } = require("purgecss-webpack-plugin");
const BundleTracker = require("webpack-bundle-tracker");
const { getPaths } = require("./utils/recursive-path.js");

module.exports = {
  watch: true,
  context: __dirname,

  entry: globAll
    .sync("./src/**/pages/**/*.{js,css,scss,html}")
    .reduce((obj, el = "") => {
      const name = path.parse(el).name;
      if (!obj[name]) obj[name] = [];
      obj[name].push(el);
      return obj;
    }, {}),

  output: {
    path: path.resolve(__dirname, "./staticfiles/js/pages/"),
    // publicPath: "auto",
    publicPath: "/",
    assetModuleFilename: "staticfiles/img/[name][ext]",
    filename: "[name].js",
  },

  module: {
    rules: [
      {
        test: /\.(sa|sc|c)ss$/,
        use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"],
      },
      {
        test: /\.html/,
        type: "asset/resource",
        generator: {
          emit: false,
        },
      },
      {
        test: /\.svg/,
        type: "asset/resource",
        generator: {
          emit: false,
        },
      },
    ],
  },

  plugins: [
    new MiniCssExtractPlugin({
      filename: "../../css/pages/[name].css",
    }),

    ...globAll.sync("./src/templates/pages/**.html").map((src) => {
      return new PurgeCSSPlugin({
        paths: globAll.sync(getPaths(src), { nodir: true }),
        only: [`/${path.parse(src).name}.`],
        fontFace: true,
        variables: true,
        keyframes: true,
        defaultExtractor: (content) => content.match(/[\w-/:]+(?<!:)/g) || [],
      });
    }),

    new BundleTracker({
      path: __dirname,
      filename: "./webpack-stats.json",
    }),
  ],
};
