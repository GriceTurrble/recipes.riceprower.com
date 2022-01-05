const colors = require('material-ui-colors')
module.exports = {
  content: [
    '../recipesite/**/*.html',
  ],
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
  plugins: [],
}
