A complete backend API built using FastAPI + PostgreSQL, implementing authentication, users, posts, activities, and admin-level operations.
Fully deployed on Railway.

🚀 Live Deployment

Base URL:
https://inkle-backend-assignment-production.up.railway.app

API Docs (Swagger):
https://inkle-backend-assignment-production.up.railway.app/docs

🛠️ Tech Stack

FastAPI

PostgreSQL (Railway)

SQLAlchemy

Pydantic

JWT Authentication

Bcrypt Password Hashing

Railway Deployment

✨ Features
🔐 Authentication

User signup

Login with JWT

Secure protected endpoints

👤 User

Create user

Get user profile

Admin: Get all users

📝 Posts

Create post

Get all posts

Get posts by user

📊 Activity

Track user actions

Get activity feed

🛡️ Admin

View all users

View all activities

🔧 Environment Variables

Add these in Railway or your .env file:

DATABASE_URL=postgresql://username:password@host:port/database
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

▶️ Run Locally
pip install -r requirements.txt
uvicorn app.main:app --reload


Swagger:
http://localhost:8000/docs

🚀 Deployment Notes (Railway)

Use this start command:

uvicorn app.main:app --host 0.0.0.0 --port $PORT


Railway will automatically build and deploy on every GitHub push.
