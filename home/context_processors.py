from django.conf import settings


def social_media_info(request):
    return {
        'INSTAGRAM_USERNAME': settings.INSTAUSERID,
        'INSTAGRAM_TOKEN': settings.INSTATOKEN
    }


def google_info(request):
    return {
        'GOOGLE_INFO': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
    }
