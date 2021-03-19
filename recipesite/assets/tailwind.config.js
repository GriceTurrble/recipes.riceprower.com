const colors = require('material-ui-colors')
module.exports = {
  // TODO Set the purge options for prod build
  // Later, set up Dockerfile to run prod builds
  purge: [
    './src/**/*.html',
    './src/**/*.jsx',
    './src/**/*.vue',
    './../**/*.html',
    './../**/*.jsx',
    './../**/*.vue',
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: { ...colors },
      screens: {
        // print styles
        'print': {'raw': 'print'},
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
