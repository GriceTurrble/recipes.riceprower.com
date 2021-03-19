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
        // Print utility styles
        // https://tailwindcss.com/docs/breakpoints#styling-for-print
        'print': {'raw': 'print'},
      },
      transitionProperty: {
        // Transform property utilities for inset properties
        // https://tailwindcss.com/docs/transition-property#property-values
        'top': 'top',
        'left': 'left',
        'right': 'right',
        'bottom': 'bottom',
        'top-left': 'top, left',
        'top-right': 'top, right',
        'bottom-left': 'bottom, left',
        'bottom-right': 'bottom, right',
      },
      zIndex: {
        // Negative value z-index utility
        // https://tailwindcss.com/docs/z-index#negative-values
        '-10': '-10',
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
