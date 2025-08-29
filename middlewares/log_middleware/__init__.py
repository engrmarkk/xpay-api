from api_services.logger import logger


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # logger.info(f"Request Method: {request.method}, Path: {request.path}")

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        # logger.info(f"Response Status Code: {response.status_code}")

        return response
