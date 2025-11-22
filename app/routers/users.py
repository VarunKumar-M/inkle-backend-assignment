from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/{user_id}/follow")
def follow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")

    target = db.query(models.User).get(user_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    existing = (
        db.query(models.Follow)
        .filter_by(follower_id=current_user.id, following_id=user_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already following")

    follow = models.Follow(
        follower_id=current_user.id,
        following_id=user_id,
    )
    db.add(follow)

    msg = f"{current_user.username} followed {target.username}"
    activity = models.Activity(
        actor_id=current_user.id,
        verb="FOLLOWED_USER",
        object_type="USER",
        object_id=target.id,
        target_user_id=target.id,
        message=msg,
    )
    db.add(activity)

    db.commit()
    return {"detail": msg}


@router.post("/{user_id}/block")
def block_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot block yourself")

    target = db.query(models.User).get(user_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    existing = (
        db.query(models.Block)
        .filter_by(blocker_id=current_user.id, blocked_id=user_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already blocked")

    block = models.Block(
        blocker_id=current_user.id,
        blocked_id=user_id,
    )
    db.add(block)
    db.commit()
    return {"detail": f"Blocked {target.username}"}
