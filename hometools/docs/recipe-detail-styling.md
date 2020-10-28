---
author: Galen Rice
date: 2020-10-27
updated: 2020-10-27
---

# Recipe detail styling

Some components of Recipe details are stored as HTML in the site database. This is done using TinyMCE, a rich-text WSYSIWYG editor in the browser.

Are your eyes glazing over already? Sorry, but the devil's in the details on this one.

Point is, the editor generates HTML that we store to the database, then output to the template on request. This means the markup it generates is *mostly* untouchable until we get it in the frontend, where we can then manipulate it with CSS and JS.

This doc describes a bit about how to work with that content so it can be styled without too many headaches.

## CSS hooks

The template file we *can* control has `<article>` and `<section>` containers around the important bits, with some of the finer details (that are *not* edited by TinyMCE) surrounded in `<span>`s with specific classes.

The basic layout of the template looks like this:

```html
<!-- recipes/templates/recipes/recipe_detail.html -->
<article class="rec-container">
  <section class="rec-header">
    <h1><!-- recipe title goes here --></h1>
    <p class="lead"><!-- recipe subtitle goes here --></p>
  </section>

  <section class="rec-description d-print-none">
    <!-- stored HTML content -->
  </section>

  <section class="rec-ingredients">
    <h2>Ingredients</h2>
    <ul class="rec-ingredient-list">
      <li class="rec-ingredient-item">
        <span class="ingredient-amount"></span>
        <span class="ingredient-amount-uom"></span>
        <span class="ingredient-type"></span>
        <span class="ingredient-preparation"></span>
      </li>
      <!-- and more <li>s for more ingredients -->
    </ul>
  </section>

  <section class="rec-directions">
    <h2>Directions</h2>
    <!-- stored HTML content -->
  </section>

  <section class="rec-footnotes">
    <h2>Footnotes</h2>
    <!-- stored HTML content -->
  </section>
</article>
```

You're free to adjust the markup for the template itself, but take care not to mess with the `{% ... %}` and `{{ ... }}` syntax: that's Django's template language, and changing those improperly can break the whole page.

Point is, you can see the markup above wraps the sections in classes that can be targeted, such as `.rec-container .rec-description`. You can go further to target the tags you might find in those sections, such as `<p>`, `<strong>`, `<em>`, `<ol>`, `<ul>`, `<li>`, `<h1>`-`<h6>`, and so on.

## Gotchas

While the TinyMCE editor is quite good at what it does, there are some circumstances where the content it generates is less than ideal for targeting with CSS. That's because some selections in the editor will apply `style` attributes to the markup. For example:

- Choosing any sort of text alignment (left, center, right, and justify) will add i.e. `style="text-align: center"`.
- It's possible to apply color to a piece of text in the editor, as well. That ends up wrapping text in `<span style="background-color: #012345;">...</span>` (some nearby content may end up with `&nbsp;`, the [non-breaking space](https://en.wikipedia.org/wiki/Non-breaking_space), but that's not a big deal).
- For unordered lists, it's possible to select a bullet style in a dropdown. That applies i.e. `style="list-style-type: square;"` to the parent `<ul>` tag.
- Using `Shift-Enter` to add spacing of any kind will inject `<br>` tags.
- Using indentation on plain paragraphs will result in `style="padding-left: 40px"` (*ew*), likely with 40px per level of indentation used.

In terms of *editing*, I recommend using the basic tools only, so the markup is left as simple as possible.

I *could* dive deeper into TinyMCE to make adjustments to the controls so it's less possible to shoot ourselves in the foot, but I'm too lazy for that. Let's just use the thing lightly and see what happens.

## Where content is generated

There are currently 3 `HTMLField` instances on the Recipe model: `description`, `directions`, and `footnotes`. Each is wrapped in `<section class="rec-[name]"></section>` for better CSS targeting.

## Where to apply styling

A stub CSS file can be found in `recipes/static/recipes/css/recipe_detail.css`. This is already included within the template, so changes in this file will affect the output of the page.

## How to test

1. Refer to the README at the project root for installation details, creating a superuser, and starting the application on the development server on your local machine.
2. Create a new Recipe through the Admin, then save it. If you need assistance navigating the Admin, let me know (it's pretty barebones right now, not the greatest UX, but something workable for making data changes).
3. View the detail page where that Recipe is displayed.
4. Make adjustments as needed, change stuff in the admin, etc.; and reload the page to see the effects.
