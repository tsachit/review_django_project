from django.conf import settings


def constants(request):
    # return any necessary values
    return {
        'PROJECT_NAME': settings.PROJECT_NAME
    }