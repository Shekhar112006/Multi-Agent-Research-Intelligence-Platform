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