from annalise_test.tracking.models import APIInteractionTracking


class APIInteractionTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.user.is_authenticated:
            return response

        # at the moment we track only api requests
        path = request.path
        if path.startswith("/api/") and not path.startswith("/api/trackings/"):
            data = request.GET if request.method != "POST" else request.POST
            APIInteractionTracking.objects.create(
                user=request.user,
                endpoint=path,
                method=request.method,
                response=response.data if response.data is None else dict(response.data),
                data=dict(data),
                cookies=request.COOKIES,
                headers=dict(response.headers),
                status_code=response.status_code,
            )

        return response
