from django import template

register = template.Library()


@register.filter( name='not' )
def not_gate(value):
    return not value
