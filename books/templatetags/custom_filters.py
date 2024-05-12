from django import template

register = template.Library()


@register.filter(name='not')
def not_gate(value):
    return not value


@register.filter(name='my_range')
def my_range(value):
    return range(1, value + 1)


@register.filter(name='is_not_object_owner')
def is_not_object_owner(request_user, object_list):
    for obj in object_list:
        if obj.user == request_user:
            return True
    return False
