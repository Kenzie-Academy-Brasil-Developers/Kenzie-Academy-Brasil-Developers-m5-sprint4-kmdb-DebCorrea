from rest_framework.exceptions import APIException
from rest_framework.views import status


class DuplicatedReviewError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Review already exists."
