from django import template

register = template.Library()

@register.filter
def repeat(value, times):
    return value * int(times)