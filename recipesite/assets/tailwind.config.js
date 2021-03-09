const colors = require('material-ui-colors')
module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: { ...colors }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
