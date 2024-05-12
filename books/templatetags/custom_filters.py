from django import template

register = template.Library()


@register.filter( name='not' )
def not_gate(value):
    return not value

@register.filter( name='my_range')
def my_range(value):
    return range(1,value+1)
