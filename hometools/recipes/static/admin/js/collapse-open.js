'use strict';
{
  window.addEventListener('load', function() {
    const fieldsets = document.querySelectorAll('fieldset.collapse.open');
    for (const [i, elem] of fieldsets.entries()) {
      elem.classList.remove('collapsed');
    }
  });
}
