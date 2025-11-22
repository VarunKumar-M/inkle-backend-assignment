# Inkle Backend Intern Assignment – Social Activity Feed

This project implements the backend for a simple social activity feed with users, posts, likes, follow/block relationships, and role-based permissions (USER / ADMIN / OWNER).

It is built with:

- **FastAPI** for the web framework
- **PostgreSQL** (e.g. Supabase) as the database
- **SQLAlchemy** as the ORM
- **JWT** authentication with `python-jose`
- **passlib[bcrypt]` for password hashing

## Features

- User signup & login with JWT-based auth
- First registered user becomes **OWNER**
- Users can:
  - Create posts
  - Like posts
  - Follow other users
  - Block other users (blocked users cannot see the blocker's activities)
- Global activity feed with entries like:
  - `ABC made a post`
  - `DEF followed ABC`
  - `PQR liked ABC's post`
  - `User deleted by 'Owner'`
  - `Post deleted by 'Admin'`
- Role-based permissions:
  - **USER** – normal actions (posts, likes, follow, block)
  - **ADMIN** – can delete posts
  - **OWNER** – can manage admins and deactivate users

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd inkle-backend-assignment
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
# source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in real values:

```bash
cp .env.example .env  # or copy manually on Windows
```

Edit `.env`:

- Set `DATABASE_URL` to your PostgreSQL / Supabase connection string
- Set `JWT_SECRET` to a strong random value

Example:

```env
DATABASE_URL=postgresql+psycopg2://postgres:password@host:5432/postgres?sslmode=require
JWT_SECRET=some_long_random_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

Open your browser at:

- Swagger UI: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Basic Usage Flow (for testing)

1. **Signup** – `POST /auth/signup`
   - First user will get `role="OWNER"`.
2. **Login** – `POST /auth/login`
   - Use the returned `access_token` as a Bearer token in Swagger (**Authorize** button).
3. **Create another user** (signup again with different username/email).
4. **Create posts** – `POST /posts`
5. **Follow a user** – `POST /users/{user_id}/follow`
6. **Like a post** – `POST /posts/{post_id}/like`
7. **Block a user** – `POST /users/{user_id}/block`
8. **View activity feed** – `GET /activity/feed`

## Admin / Owner Endpoints

- Promote user to admin – `POST /admin/users/{user_id}/make-admin` (OWNER only)
- Demote admin to user – `POST /admin/users/{user_id}/remove-admin` (OWNER only)
- Deactivate a user – `DELETE /admin/users/{user_id}` (OWNER only)
- Delete a post – `DELETE /posts/{post_id}` (ADMIN or OWNER)

## Postman Documentation

You can create a Postman collection that mirrors the endpoints:

- `/auth/signup`
- `/auth/login`
- `/users/me`
- `/users/{id}`
- `/users/{id}/follow`
- `/users/{id}/block`
- `/posts`
- `/posts/{id}`
- `/posts/{id}/like`
- `/activity/feed`
- `/admin/users/{id}/make-admin`
- `/admin/users/{id}/remove-admin`
- `/admin/users/{id}` (DELETE)

Export the collection and share it as part of the assignment if needed.

## Deployment

You can deploy this API on platforms like **Render**, **Railway**, or a **VM (EC2)**:

1. Push the code to GitHub.
2. Create a new web service on your chosen platform.
3. Set environment variables from `.env` (particularly `DATABASE_URL`, `JWT_SECRET`).
4. Use the start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Use the deployed URL (e.g. `https://your-app.onrender.com`) as the public link for the assignment submission.
