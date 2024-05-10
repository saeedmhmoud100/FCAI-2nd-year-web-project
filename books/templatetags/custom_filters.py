from django import template

register = template.Library()


@register.filter( name='not_gate' )
def not_gate(value):
    return not value
