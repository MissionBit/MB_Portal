from django.core.exceptions import PermissionDenied


def group_required(group):
    def user_in_group(func):
        def wrapper(request, *args, **kwargs):
            print(request.user.groups.all())
            if request.user.groups.filter(name=group).exists():
                return func(request, *args, **kwargs)
            else:
                print("HERE RAISING PERMISSION DENIED")
                raise PermissionDenied

        return wrapper

    return user_in_group
