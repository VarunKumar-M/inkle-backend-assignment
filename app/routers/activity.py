from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from .. import models, schemas
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/activity", tags=["activity"])


@router.get("/feed", response_model=list[schemas.ActivityOut])
def get_feed(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Users who have blocked the current user should not have their activities visible
    subquery = (
        db.query(models.Block.blocker_id)
        .filter(models.Block.blocked_id == current_user.id)
        .subquery()
    )

    activities = (
        db.query(models.Activity)
        .filter(~models.Activity.actor_id.in_(subquery))
        .order_by(models.Activity.created_at.desc())
        .limit(100)
        .all()
    )
    return activities
