from staff.staff_views_helper import get_classroom_by_django_user


def user_groups(request):
    user_groups = set(request.user.groups.all().values_list("name", flat=True))
    return {"user_groups": user_groups}


def user_classroom(request):
    classroom = get_classroom_by_django_user(request.user)
    return {"classroom": classroom}
