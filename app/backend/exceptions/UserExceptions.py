from .base import AppException

class UserExists(AppException):
    def __init__(self):
        super().__init__('This user already exists')