from typing import Callable, TypeVar

from django.http import HttpRequest
from django.http.response import HttpResponseBase

from annalise_test.tracking.models import APIInteractionTracking


ResponseType = TypeVar("ResponseType", bound=HttpResponseBase)
RequestType = TypeVar("RequestType", bound=HttpRequest)


class APIInteractionTrackingMiddleware:
    """
    Track user interactions with API routes.
    Do not track `/api/trackings/` route.
    """

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: RequestType) -> ResponseType:
        response: ResponseType = self.get_response(request)

        if not request.user.is_authenticated:
            return response

        # at the moment we track only api requests
        path: str = request.path
        if path.startswith("/api/") and not path.startswith("/api/trackings/"):
            APIInteractionTracking.objects.create(
                user=request.user,
                endpoint=path,
                method=request.method,
                response=response.data if response.data is None else dict(response.data),
                data=dict(request.GET if request.method != "POST" else request.POST),
                cookies=request.COOKIES,
                headers=dict(response.headers),
                status_code=response.status_code,
            )

        return response
