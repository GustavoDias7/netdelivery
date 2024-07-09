const path = require("path");
const glob = require("glob-all");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const { PurgeCSSPlugin } = require("purgecss-webpack-plugin");
const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  watch: true,
  mode: "production", // development | production
  context: __dirname,

  entry: glob.sync("./src/**/pages/**/*.{js,css,scss,html}").reduce((obj, el = "") => {
    const name = path.parse(el).name;
    if (!obj[name]) obj[name] = [];
    obj[name].push(el);
    return obj
  }, {}),

  output: {
    path: path.resolve(__dirname, "./staticfiles/js/pages/"),
    publicPath: "auto",
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
        type: 'asset/resource',
        generator: {
          emit: false,
        }
      },
    ],
  },

  plugins: [
    new MiniCssExtractPlugin({
      filename: "../../css/pages/[name].css",
    }),

    ...glob.sync("./src/templates/pages/**.html").map((src) => {
      return new PurgeCSSPlugin({
        paths: glob.sync(src, { nodir: true }),
        only: [path.parse(src).name],
        fontFace: true,
        variables: true,
        keyframes: true,
        defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || []
      });
    }),

    new BundleTracker({
      path: __dirname,
      filename: "./webpack-stats.json",
    }),
  ],
};