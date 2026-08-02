"""
Paper router.
"""

from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies.auth import get_current_user
from app.modules.papers.services.paper_service import PaperService
from app.modules.users.models.users import User

router = APIRouter(
    prefix="/projects",
    tags=["Papers"],
)


@router.post("/{project_id}/papers")
async def upload_paper(
    project_id: UUID,
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PaperService(db)

    return await service.upload(
        project_id=project_id,
        current_user=current_user,
        title=title,
        file=file,
    )