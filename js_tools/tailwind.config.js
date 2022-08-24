const colors = require("material-ui-colors");
const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  content: [
    "../*.html",
    "../*.md",
    "../_layouts/**/*.html",
    "../_layouts/**/*.md",
    "../_tabs/**/*.html",
    "../_tabs/**/*.md",
  ],
  theme: {
    extend: {
      colors: { ...colors }
    },
  },
  plugins: [require("@tailwindcss/typography")]
};
