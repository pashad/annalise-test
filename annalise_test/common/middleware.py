from typing import Callable, TypeVar

from django.http import HttpResponseForbidden, HttpRequest
from django.http.response import HttpResponseBase

from annalise_test import settings


ResponseType = TypeVar('ResponseType', bound=HttpResponseBase)
RequestType = TypeVar('RequestType', bound=HttpRequest)


class MediaRestrictedAccessMiddleware:
    """ Restrict access to media files for non-authenticated users. """

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: RequestType) -> ResponseType:
        if request.path.startswith(f"/{settings.MEDIA_URL}") and not request.user.is_authenticated:
            return HttpResponseForbidden()
        response: ResponseType = self.get_response(request)
        return response
