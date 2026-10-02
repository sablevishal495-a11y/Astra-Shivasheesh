# ASTRA Backend (Google Auth & PostgreSQL)

## Setup & Run

1. **Activate Virtual Environment & Run Server:**
   ```bash
   cd backend
   ./venv/bin/python app.py
   ```
   Server runs at: `http://localhost:5001`

2. **Configure Database & Google OAuth:**
   Edit `.env` with your credentials:
   - `DATABASE_URL`: Your PostgreSQL connection string (Local or cloud e.g., Neon / Supabase).
   - `GOOGLE_CLIENT_ID`: OAuth 2.0 Web Client ID from Google Cloud Console.

3. **Endpoints:**
   - `GET  /api/health` - Server and PostgreSQL connection check.
   - `POST /api/auth/google` - Verify Google credential and persist user.
