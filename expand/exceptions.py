from rest_framework.exceptions import APIException

class ImproperExpandException(APIException):
    status_code = 500
    default_detail = 'The expansion mapping was not configured properly'

