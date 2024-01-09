import logging

logger = logging.getLogger(__name__)

class RequestResponseLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request
        logger.info(f"Request: {request.method} {request.get_full_path()}")

        # Get the response
        response = self.get_response(request)

        # Log the response
        logger.info(f"Response: {response.status_code} {response.reason_phrase}")

        return response
