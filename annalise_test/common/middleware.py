from django.http import HttpResponseForbidden

from annalise_test import settings


class MediaRestrictedAccessMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(f"/{settings.MEDIA_URL}") and not request.user.is_authenticated:
            return HttpResponseForbidden()
        response = self.get_response(request)
        return response