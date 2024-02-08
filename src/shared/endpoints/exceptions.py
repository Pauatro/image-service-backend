from fastapi import HTTPException, status


class InternalServerHttpException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class UnauthorizedHttpException(HTTPException):
    def __init__(self, detail, headers):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers=headers,
        )


class ForbiddenHttpException(HTTPException):
    def __init__(self, detail, headers):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers=headers,
        )


class ResourceNotFoundHttpException(HTTPException):
    def __init__(self, detail="The requested resource was not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )
