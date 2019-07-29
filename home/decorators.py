from django.core.exceptions import PermissionDenied


def group_required(group):
    def user_in_group(func):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name=group).exists():
                return func(request, *args, **kwargs)
            else:
                raise PermissionDenied

        return wrapper

    return user_in_group


def group_required_multiple(group_list):
    def user_in_group(func):
        def wrapper(request, *args, **kwargs):
            group = [group for group in request.user.groups.all() if group in group_list]
            if group is not None:
                return func(request, *args, **kwargs)
            else:
                raise PermissionDenied

        return wrapper

    return user_in_group
