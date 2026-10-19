# Moneta frontend

A responsive React + TypeScript dashboard for the Expense Tracker API. It includes registration and sign in, monthly income/expense summaries, transaction search and filtering, CSV export, and full transaction create, edit, and delete flows.

## Run locally

1. Start the API from the repository root after configuring its database and secret key:

   ```bash
   python -m pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. In another terminal, install and start the frontend:

   ```bash
   cd frontend
   npm install
   Copy-Item .env.example .env.local
   npm run dev
   ```

3. Open the Vite URL shown in the terminal (usually `http://localhost:5173`).

Set `VITE_API_URL` in `frontend/.env.local` to the API origin when it is not running at `http://127.0.0.1:8000`. On the API deployment, set `FRONTEND_ORIGINS` to a comma-separated list of allowed frontend origins.

The dashboard displays amounts in USD. Change the currency formatter in `src/App.tsx` if your account uses another currency.
