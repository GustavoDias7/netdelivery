const fs = require("fs");
const path = require("path");
const globAll = require("glob-all");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const { PurgeCSSPlugin } = require("purgecss-webpack-plugin");
const BundleTracker = require("webpack-bundle-tracker");
const { extractExtendsPaths, extractIncludePaths } = require("./utils");

module.exports = {
  watch: true,
  mode: "production", // development | production
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
    publicPath: '/',
    assetModuleFilename: 'staticfiles/img/[name][ext]',
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
      // access the content of extends and includes associated to the pages
      const data = fs.readFileSync(src);
      const dirPath = path.parse(src).dir;
      const extendsPathFromPage = extractExtendsPaths("" + data)[0];
      const includesPathsFromPage = extractIncludePaths("" + data).map((p) => {
        return path.join(dirPath, p);
      });
      const basePathFromPage = path.join("./", dirPath, extendsPathFromPage);
      const data2 = fs.readFileSync(basePathFromPage);
      const includesPaths = extractIncludePaths("" + data2).map((p) => {
        return path.join(dirPath, "..", p);
      });
      includesPaths.push(basePathFromPage);
      includesPaths.push(src);

      return new PurgeCSSPlugin({
        paths: globAll.sync([...includesPaths, ...includesPathsFromPage], { nodir: true }),
        only: [path.parse(src).name],
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