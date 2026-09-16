# Expense Tracker API

FastAPI midterm assignment implementing JWT authentication and protected transaction CRUD with SQLAlchemy.

## Features

- User registration with bcrypt password hashing
- OAuth2 password login with JWT access tokens
- User-owned income and expense transactions
- Create, list, retrieve, update, and delete transactions
- Filtering by type, category, minimum amount, and maximum amount
- Five pytest cases covering transaction CRUD
- SQLite for local development and PostgreSQL through `DATABASE_URL`

## Run locally

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Open Swagger at http://127.0.0.1:8000/docs.

## Use the API

1. Call `POST /auth/register`:

```json
{
  "username": "student1",
  "email": "student1@example.com",
  "password": "Password123!"
}
```

2. Call `POST /auth/login` using form fields `username` and `password`.
3. Click **Authorize** in Swagger and enter the returned token as `Bearer <token>`.
4. Use the protected `/transactions` endpoints.

Example transaction:

```json
{
  "title": "Lunch",
  "amount": 25.5,
  "type": "expense",
  "category": "Food"
}
```

Filtering example:

`GET /transactions/filter?type=expense&category=Food&minimum_amount=10`

## PostgreSQL and Render

Set the environment variables:

- `DATABASE_URL=postgresql+psycopg2://user:password@host:5432/database`
- `SECRET_KEY=<long-random-secret>`

Render start command:

```text
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Tests

```powershell
pytest -q
```
