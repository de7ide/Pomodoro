class UserNotFoundException(Exception):
    detail = "User not found"


class UserNotFoundPasswordException(Exception):
    detail = "Password is not correct"


class TokenExpire(Exception):
    detail = "Token has expired"


class TokenInvalide(Exception):
    detail = "Token is not correct"


class TaskNotFound(Exception):
    detail = "Task is not found"