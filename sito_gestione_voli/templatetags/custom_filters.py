from django import template

register = template.Library()

@register.filter
def groupby(value, arg):
    result = []
    for i in range(0, len(value), arg):
        result.append(value[i:i + arg])
    return result
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)