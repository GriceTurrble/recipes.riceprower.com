const colors = require("material-ui-colors");
const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  content: [
    "../*.html",
    "../*.md",
    "../_layouts/**/*.html",
    "../_layouts/**/*.md",
    "../_includes/**/*.html",
    "../_includes/**/*.md"
  ],
  theme: {
    fontFamily: {
      sans: ["'Work Sans'", ...defaultTheme.fontFamily.sans],
      serif: ["'Modern Antiqua'", ...defaultTheme.fontFamily.sans]
    },
    extend: {
      colors: { ...colors }
    }
  },
  plugins: [require("@tailwindcss/typography"), require("@tailwindcss/forms")]
};
