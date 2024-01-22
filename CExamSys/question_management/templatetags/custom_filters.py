from django import template

register = template.Library()

@register.filter(name='first_line')
def first_line(value):
    """Return the first line of a string."""
    return value.split('\n')[0] if value else ''
