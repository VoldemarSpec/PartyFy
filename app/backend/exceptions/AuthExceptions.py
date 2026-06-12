from .base import AppException

class InvalidCredentials(AppException):
    def __init__(self):
        super().__init__('Invalid credentials')