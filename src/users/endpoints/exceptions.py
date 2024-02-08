from shared.endpoints.exceptions import (
    UnauthorizedHttpException,
    ForbiddenHttpException,
    ResourceNotFoundHttpException,
)


class IncorrectUsernameOrPasswordHttpException(UnauthorizedHttpException):
    def __init__(self):
        super().__init__(
            detail="Incorrect username or password",
        )


class UserNotFoundHttpException(ResourceNotFoundHttpException):
    def __init__(self):
        super().__init__(
            detail="The requested user was not found",
        )


class ExpiredTokenHttpException(UnauthorizedHttpException):
    def __init__(self):
        super().__init__(
            detail="Expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidTokenHttpException(ForbiddenHttpException):
    def __init__(self):
        super().__init__(
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
