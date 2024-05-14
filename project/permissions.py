from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url


def check_user(user):

    return user.is_authenticated


def check_authenticated(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not test_func(request.user):
                messages.add_message(request, messages.ERROR, 'You need to login to view this page')
                path = request.build_absolute_uri()
                resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
                return HttpResponseRedirect('%s?%s=%s' % (resolved_login_url, redirect_field_name, path))
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator



def is_not_authenticated(user):
    return user.is_anonymous
def is_admin(user):
    return user.is_superuser