from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models
from ..deps import get_db, require_admin, require_owner

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/users/{user_id}/make-admin")
def make_admin(
    user_id: int,
    db: Session = Depends(get_db),
    owner_user: models.User = Depends(require_owner),
):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = "ADMIN"
    db.commit()
    return {"detail": "User promoted to admin"}


@router.post("/users/{user_id}/remove-admin")
def remove_admin(
    user_id: int,
    db: Session = Depends(get_db),
    owner_user: models.User = Depends(require_owner),
):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role != "ADMIN":
        raise HTTPException(status_code=400, detail="User is not an admin")
    user.role = "USER"
    db.commit()
    return {"detail": "User demoted to user"}


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_as_owner(
    user_id: int,
    db: Session = Depends(get_db),
    owner_user: models.User = Depends(require_owner),
):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False

    msg = "User deleted by 'Owner'"
    activity = models.Activity(
        actor_id=owner_user.id,
        verb="USER_DELETED",
        object_type="USER",
        object_id=user.id,
        target_user_id=user.id,
        message=msg,
    )
    db.add(activity)
    db.commit()
    return
