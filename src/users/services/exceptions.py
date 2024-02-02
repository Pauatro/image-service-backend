class UserNotFoundException(Exception):
    pass

class UserAlreadyExistsException(Exception):
    pass

class IncorrectUsernameOrPasswordException(Exception):
    pass