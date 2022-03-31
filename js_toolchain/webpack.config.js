const path = require("path");
const isProduction = process.env.NODE_ENV === "production";
const djangoAppName = "recipesite";
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

const config = {
  entry: "./src/index.js",
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "..", djangoAppName, "static", "js"),
    clean: true
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "../css/styles.css"
    })
  ],
  module: {
    rules: [
      {
        test: /\.css$/i,
        exclude: /node_modules/,
        use: [MiniCssExtractPlugin.loader, "css-loader", "postcss-loader"]
      }
    ]
  }
};

module.exports = () => {
  if (isProduction) {
    config.mode = "production";
  } else {
    config.mode = "development";
  }
  return config;
};
