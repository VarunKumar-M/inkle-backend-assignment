from fastapi import FastAPI

from .database import Base, engine
from .routers import auth_router, users, posts, activity, admin

# Create all tables in the configured database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inkle Backend Intern Assignment")


@app.get("/")
def read_root():
    return {"message": "Inkle backend is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(auth_router.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(activity.router)
app.include_router(admin.router)
