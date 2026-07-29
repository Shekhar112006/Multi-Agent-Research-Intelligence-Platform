"""
User-related enumerations.

This module contains enumerations used by the User model.
"""

from enum import Enum


class UserRole(str, Enum):
    """
    Roles available in the application.

    These roles are used for Role-Based Access Control (RBAC).
    """

    ADMIN = "admin"
    RESEARCHER = "researcher"
    STUDENT = "student"