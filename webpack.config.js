const path = require("path");
const globAll = require("glob-all");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const { PurgeCSSPlugin } = require("purgecss-webpack-plugin");
const { getPaths } = require("./utils/recursive-path.js");
const { DefinePlugin } = require("webpack");

module.exports = {
  context: __dirname,
  entry: globAll
    .sync(["./src/**/pages/**/*.{js,css,scss}"])
    .reduce((obj, el = "") => {
      const name = path.parse(el).name;
      if (!obj[name]) obj[name] = [];
      obj[name].push(el);
      return obj;
    }, {}),

  output: {
    path: path.resolve(__dirname, "./static/js/pages/"),
    publicPath: "/",
    filename: "[name].js",
    clean: true,
  },

  module: {
    rules: [
      {
        test: /\.(sa|sc|c)ss$/,
        use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"],
      },
      {
        test: /\.html$/,
        type: "asset/resource",
        generator: {
          emit: false,
          filename: ({ runtime }) =>
            runtime === "index"
              ? "../../[name][ext]"
              : "../../[name]/index[ext]",
        },
      },
      {
        test: /\.(svg|png|jpg|gif)$/i,
        type: "asset/resource",
        generator: {
          emit: false,
          filename: "static/img/[name][ext]",
        },
      },
    ],
  },

  plugins: [
    new DefinePlugin({
      __VUE_OPTIONS_API__: true,
      __VUE_PROD_DEVTOOLS__: true,
      __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: "false",
    }),

    new MiniCssExtractPlugin({
      filename: "../../css/pages/[name].css",
    }),

    ...globAll.sync("./src/templates/pages/**/*.html").map((src) => {
      return new PurgeCSSPlugin({
        paths: globAll.sync(getPaths(src), { nodir: true }),
        only: [`/${path.parse(src).name}.`],
        fontFace: true,
        variables: true,
        keyframes: true,
        defaultExtractor: (content) => content.match(/[\w-/:]+(?<!:)/g) || [],
        safelist: {
          standard: ["swiper", /^swiper-/],
        },
      });
    }),
  ],
};