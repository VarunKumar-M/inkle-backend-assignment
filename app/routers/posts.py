from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from .. import models, schemas
from ..deps import get_db, get_current_user, require_admin

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("", response_model=schemas.PostOut)
def create_post(
    post_in: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    post = models.Post(
        author_id=current_user.id,
        content=post_in.content,
    )
    db.add(post)
    db.flush()  # Get post.id before commit

    msg = f"{current_user.username} made a post"
    activity = models.Activity(
        actor_id=current_user.id,
        verb="POST_CREATED",
        object_type="POST",
        object_id=post.id,
        target_user_id=current_user.id,
        message=msg,
    )
    db.add(activity)
    db.commit()
    db.refresh(post)
    return post


@router.get("", response_model=list[schemas.PostOut])
def list_posts(db: Session = Depends(get_db)):
    posts = (
        db.query(models.Post)
        .filter(models.Post.is_deleted == False)
        .order_by(models.Post.created_at.desc())
        .all()
    )
    return posts


@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(post_id)
    if not post or post.is_deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/{post_id}/like")
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    post = db.query(models.Post).get(post_id)
    if not post or post.is_deleted:
        raise HTTPException(status_code=404, detail="Post not found")

    existing = (
        db.query(models.Like)
        .filter_by(user_id=current_user.id, post_id=post_id, is_deleted=False)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already liked")

    like = models.Like(user_id=current_user.id, post_id=post_id)
    db.add(like)

    author = db.query(models.User).get(post.author_id)
    msg = f"{current_user.username} liked {author.username}'s post"
    activity = models.Activity(
        actor_id=current_user.id,
        verb="LIKED_POST",
        object_type="POST",
        object_id=post.id,
        target_user_id=author.id,
        message=msg,
    )
    db.add(activity)
    db.commit()
    return {"detail": msg}


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_as_admin(
    post_id: int,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(require_admin),
):
    post = db.query(models.Post).get(post_id)
    if not post or post.is_deleted:
        raise HTTPException(status_code=404, detail="Post not found")

    post.is_deleted = True
    post.deleted_by_role = admin_user.role
    post.updated_at = datetime.utcnow()

    msg = f"Post deleted by '{admin_user.role}'"
    activity = models.Activity(
        actor_id=admin_user.id,
        verb="POST_DELETED",
        object_type="POST",
        object_id=post.id,
        target_user_id=post.author_id,
        message=msg,
    )
    db.add(activity)
    db.commit()
    return
