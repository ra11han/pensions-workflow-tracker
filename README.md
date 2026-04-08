# Pensions Workflow Tracker (Django)

A Django web application that tracks workflow cases in a shared team queue.

## Key features (MVP)

- Shared **Case** list (everyone sees the same workflow)
- Create / edit cases, update status, assign to a user
- Case detail page with **notes** timeline (audit trail)
- Basic filters (status, priority, scheme, assigned)
- Login/register/logout
- Admin can delete cases and manage reference data (schemes/statuses) via Django admin

## Local setup

1. Create a virtual environment and install dependencies:

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

2. Create database + seed demo data:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

By default in local dev (DJANGO_DEBUG=true), the app will seed reference data (Statuses/Schemes) and sample Cases if `SEED_DEMO_DATA=true`.

## GitHub (push your code)

GitHub provides instructions for adding locally hosted code and pushing commits to a remote repository. See:

- Adding locally hosted code to GitHub: https://docs.github.com/articles/adding-an-existing-project-to-github-using-the-command-line
- Pushing commits to a remote repository: https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository

Typical command-line flow (summary):

```bash
git init -b main
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## Deploying to Render

Render’s Django deployment guide explains:

- Using `DATABASE_URL` via `dj-database-url`
- Serving static files with WhiteNoise
- Creating a `build.sh` that runs `pip install`, `collectstatic`, and `migrate`
- Configuring a web service with build/start commands and environment variables

Guide: https://render.com/docs/deploy-django

Quick steps (manual dashboard option):

- Create a new **PostgreSQL database** and copy its internal database URL.
- Create a new **Web Service**, connect your GitHub repo, and set:
  - **Build Command**: `./build.sh`
  - **Start Command**: `python -m gunicorn pensions_tracker.wsgi:application`
- Add environment variables:
  - `DATABASE_URL` = your Render database internal URL
  - `SECRET_KEY` = generate a secure value
  - `WEB_CONCURRENCY` = 2

Alternatively, you can deploy using the included `render.yaml` blueprint file (see Render docs for blueprints).

## Admin & credentials

- Create an admin user locally with `python manage.py createsuperuser`.
- In Render, you can create a superuser using the Render shell, as described in Render’s Django guide.
