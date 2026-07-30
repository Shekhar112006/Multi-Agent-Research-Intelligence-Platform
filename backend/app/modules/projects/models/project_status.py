"""
Project status enumeration.
"""

from enum import Enum


class ProjectStatus(str, Enum):
    """
    Available project states.
    """

    ACTIVE = "active"
    ARCHIVED = "archived"