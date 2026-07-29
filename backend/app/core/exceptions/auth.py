"""
Authentication related exceptions.
"""


class EmailAlreadyExistsError(Exception):
    """
    Raised when attempting to register
    with an email that already exists.
    """

    def __init__(self):
        super().__init__("Email already registered.")

class InvalidCredentialsError(Exception):
    """
    Raised when login credentials are invalid.
    """

    def __init__(self):
        super().__init__("Invalid email or password.")