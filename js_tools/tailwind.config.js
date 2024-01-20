const colors = require("material-ui-colors");
const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  corePlugins: {
    preflight: false,
  },
  content: [
    "../*.{html,md}",
    "../overrides/**/*.{html,md}"
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
