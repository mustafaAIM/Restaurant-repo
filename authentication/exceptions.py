
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None and isinstance(response.data, dict):
        custom_response = {"message": {}}
        for key, value in response.data.items():
            if isinstance(value, list) and len(value) > 0:
                custom_response["message"] = str(value[0])
            else:
                custom_response["message"] = str(value)
        response.data = custom_response
    return response
