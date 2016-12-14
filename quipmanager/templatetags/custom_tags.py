from django import template

register = template.Library()

# @register.filter
# def index(sequence, position):
#     return sequence[position]


@register.simple_tag
def iloc(item, *args):
    '''
    Get an element of a template variable (assumed that it is a list) using the index
    2d indexing supported
    '''
    for arg in args:
        item = item[arg]
    return item