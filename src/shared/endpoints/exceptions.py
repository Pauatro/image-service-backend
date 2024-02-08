from fastapi import HTTPException, status


class InternalServerHttpException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class ResourceNotFoundHttpException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested resource was not found",
        )
