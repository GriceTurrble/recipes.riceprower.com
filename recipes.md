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
  class="grid grid-flow-row-dense gap-2
         grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
>
{% for page in site.recipes %}
  {% assign num=20 %}
  {% for i in (1..num) %}
  <a
    href="{{ page.url }}"
    class="
      block
      px-6
      py-2
      border border-deepPurple-A100
      w-full
      hover:bg-deepPurple-500 hover:text-white
      focus:outline-none focus:ring-0 focus:bg-gray-200 focus:text-gray-600
      transition
      ease-in-out
      rounded-lg
      cursor-pointer
      no-underline
    "
  >{{ page.title }}</a>
  {% endfor %}
{% endfor %}
</div>
