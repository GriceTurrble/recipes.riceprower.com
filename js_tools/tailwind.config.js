const colors = require("material-ui-colors");
const defaultTheme = require("tailwindcss/defaultTheme");
/** @type {import('tailwindcss').Config} */

module.exports = {
  corePlugins: {
    preflight: false,
  },
  content: [
    "../overrides/**/*.{html,md}",
    "../includes/**/*.{html,md}",
    "../docs/**/*.{html,md}",
  ],
  theme: {
    fontFamily: {
      sans: ["'Work Sans'", ...defaultTheme.fontFamily.sans],
      serif: ["'Modern Antiqua'", ...defaultTheme.fontFamily.sans]
    },
    extend: {
      colors: { ...colors },
      // Customizing typography's raw css for prose.
      // Ref: https://tailwindcss.com/docs/typography-plugin#customizing-the-css
      typography: {
        DEFAULT: {
          css: {
            "line-height": "1.6",
            "--tw-prose-bold": "var(--md-typeset-color)",
            "--tw-prose-body": "var(--md-typeset-color)",
            "--tw-prose-links": "var(--md-typeset-a-color)",
          }
        }
      },
      screens: {
        "xl": "1220px"
      }
    }
  },
  plugins: [require("@tailwindcss/typography"), require("@tailwindcss/forms")]
};
