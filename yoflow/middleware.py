import traceback

from django.conf import settings
from django.http import JsonResponse

from yoflow.exceptions import FlowException


class YoflowMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, FlowException):
            if settings.DEBUG:
                traceback.print_exc()
            status = exception.status_code
            payload = exception.to_dict()
            return JsonResponse(payload, status=status)
