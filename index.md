---
title: Home
layout: default
---
# Recipes from the Rice-Prower household

These are the things I know I know, *these* are the things I know.

<!-- Site search, powered by Algolia -->
<div id="sitesearch-search-box"></div>
<div id="sitesearch-hits"></div>
<div id="sitesearch-pagination-container" class="not-prose"></div>

<script>
  const search = instantsearch({
    appId: '{{ site.algolia.application_id }}',
    apiKey: '{{ site.algolia.search_api_key }}',
    indexName: '{{ site.algolia.index_name }}',
    routing: true
  });

  // initialize SearchBox
  const searchBoxWidget = instantsearch.widgets.searchBox({
    container: '#sitesearch-search-box',
    placeholder: 'Find something good...',
    autofocus: true,
    magnifier: false,
    reset: false,
    cssClasses: {
      input: "searchbox-input",
    }
  });
  /* {% comment %}
    Let's talk about these `cssClasses` settings.

    Tailwind usually wants us to dictate the CSS classes in the markup.
    Therefore, it might seem seem wise to include all the style utilities we want here.

    Unfortunately, we don't have complete control over which elements are added to the markup
    using these widgets: we may want to add styles to an <a> tag that is active, but the widget
    for that only lets us adjust the containing <li>.

    So, the majority of these styles are defined in js_tools/src/styles.css, as nested rules
    with @apply directives. This provides a few benefits:
    1. We know where all the styles are defined, and have more granular control over how those
       styles get applied in the final output.
    2. The JS code needs a much smaller set of template code to swap around.
    3. We get a better IDE experience for those CSS classes when editing in a CSS file.
       We'd have a similar experience editing within HTML or Markdown contexts, but
       these JS sections don't follow those same language rules.
  {% endcomment %} */
  search.addWidget(searchBoxWidget);

  // initialize hits widget
  const hitBoxWidget = instantsearch.widgets.hits({
    container: '#sitesearch-hits',
    templates: {
      empty: 'No results',
      item: `{% include recipe/search_item.html %}`
    }
  });
  search.addWidget(hitBoxWidget);

  const paginationWidget = instantsearch.widgets.pagination({
    container: '#sitesearch-pagination-container',
    cssClasses: {
      item: 'page-item',
      link: 'page-link',
      active: 'active',
      disabled: 'disabled',
    }
  });
  search.addWidget(paginationWidget);

  search.start();
</script>
