---
title: Stuff!
permalink: /r/all
layout: default
redirect_from:
  - /r/
---
{% include recipe_breadcrumb.html %}

# All Recipes (but not allrecipes)

These are the things I know I know, *these* are the things I know.

<div
  class="columns-1 sm:columns-2 lg:columns-3 xl:columns-4 gap-4"
>
{% for page in site.recipes %}
  {% assign num=0 %}
  {% for thing in (i..num) %}
  {% include recipe_list_card.html page=page %}
  {% endfor %}
{% endfor %}
</div>
