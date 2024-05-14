from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test


def check_user(user):
    # Replace this with your own test
    return user.is_authenticated


def check_authenticated(test_func, login_url=None, redirect_field_name=None):
    def decorator(view_func):
        @user_passes_test(test_func, login_url=login_url, redirect_field_name=redirect_field_name)
        def _wrapped_view(request, *args, **kwargs):
            if not test_func(request.user):
                messages.error(request, 'You need to login to view this page')
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
