class UserNotFoundException(Exception):
    detail = "User not found"

class UserNotFoundPasswordException(Exception):
    detail = "Password is not correct"