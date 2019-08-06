from django.conf import settings


def social_media_info(request):
    return {
        'INSTAGRAM_USERNAME': settings.INSTAUSERID,
        'INSTAGRAM_TOKEN': settings.INSTATOKEN
    }
