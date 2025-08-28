# create a django function that returns http response
from rest_framework.response import Response


def return_response(
    message: str, status_message: str, status: int = 200, data=None
) -> Response:
    res = {
        "message": message,
        "status": status_message,
    }
    if data is not None:
        res["data"] = data
    return Response(res, status=status)
