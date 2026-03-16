from functools import wraps
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect


# Decorator for groups
# def group_required(allowed_groups=None):
#     if allowed_groups is None:
#         allowed_groups = []
#
#     def decorator(view_func):
#         @wraps(view_func)
#         def wrap(request, *args, **kwargs):
#             if not request.user.is_authenticated:
#                 messages.error(request, 'You must be logged in to access this page.')
#                 return redirect(f'{reverse('accounts:accountlogin')}?next={request.path}')
#
#             user_group = None
#             if request.user.is_superuser or request.user.is_administrator:
#                 user_group = 'Administrators'
#             elif request.user.is_employee:
#                 user_group = 'Employees'
#             elif request.user.is_dentist:
#                 user_group = 'Dentists'
#             elif request.user.is_patient:
#                 user_group = 'Patients'
#
#             if user_group in allowed_groups:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 messages.error(request, 'You don\'t have the permission to view this page.')
#                 referer_url = request.META.get('HTTP_REFERER')
#                 if referer_url:
#                     return redirect(referer_url)
#                 else:
#                     return redirect('mimascompany:index')
#         return wrap
#     return decorator
def group_required(allowed_groups=None):
    if allowed_groups is None:
        allowed_groups = []

    def decorator(view_func):
        @wraps(view_func)
        def wrap(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'You must be logged in to access this page.')
                return redirect(f'{reverse('accounts:accountlogin')}?next={request.path}')

            # --- UPDATED LOGIC ---
            # Check if user's type matches the required group string
            user_group = request.user.user_type

            # If you want superusers to always pass, keep this:
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            # ---------------------

            if user_group in allowed_groups:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'You don\'t have the permission to view this page.')
                referer_url = request.META.get('HTTP_REFERER')
                if referer_url:
                    return redirect(referer_url)
                else:
                    return redirect('mimascompany:index')
        return wrap
    return decorator
