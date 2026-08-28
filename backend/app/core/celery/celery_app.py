"""
Celery application configuration.
"""

from celery import Celery

from app.core.config.settings import settings

# Register all SQLAlchemy models
import app.core.database.models


celery_app = Celery(
    "mrip",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.autodiscover_tasks(
    [
        "app.modules.processing",
    ]
)