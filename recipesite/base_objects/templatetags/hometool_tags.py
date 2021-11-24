from typing import Optional

from django import template

register = template.Library()


@register.filter(name="split")
def split(value, arg: Optional[str] = None) -> list:
    """Implement str.split() as a template filter.

    Example:

        {% with words="Whatever man!" %}
          {% for word in words|split %}
            <span>{{ word }}</span>
          {% endfor %}
        {% endwith %}

    Output:

        <span>Whatever</span>
        <span>man!</span>

    Providing an argument to the filter will pass that same arg to `.split`. Example:

        {% with fruits="apple,pear,banana" %}
          {% for fruit in fruits|split:',' %}
            <span>{{ fruit }}</span>
          {% endfor %}
        {% endwith %}

    Outputs:

        <span>apple</span>
        <span>pear</span>
        <span>banana</span>
    """
    if not value:
        return []
    return str(value).split(arg)
