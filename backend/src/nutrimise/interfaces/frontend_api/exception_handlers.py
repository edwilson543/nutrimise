from fastapi import requests, responses, status


def object_does_not_exist(
    request: requests.Request, exc: Exception
) -> responses.JSONResponse:
    return responses.JSONResponse(
        content={"message": "The requested resource does not exist."},
        status_code=status.HTTP_404_NOT_FOUND,
    )
