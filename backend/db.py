import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/astradb")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    """Initializes users table in PostgreSQL."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        google_id VARCHAR(255) UNIQUE,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        username VARCHAR(255),
                        avatar_url TEXT,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                conn.commit()
        return True, "Database initialized successfully"
    except Exception as e:
        return False, str(e)

def upsert_google_user(google_id, email, username, avatar_url):
    """Inserts or updates user from Google OAuth profile."""
    query = """
        INSERT INTO users (google_id, email, username, avatar_url, last_login)
        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (email) DO UPDATE SET
            google_id = COALESCE(EXCLUDED.google_id, users.google_id),
            username = COALESCE(EXCLUDED.username, users.username),
            avatar_url = COALESCE(EXCLUDED.avatar_url, users.avatar_url),
            last_login = CURRENT_TIMESTAMP
        RETURNING id, google_id, email, username, avatar_url, created_at, last_login;
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (google_id, email, username, avatar_url))
            user = cur.fetchone()
            conn.commit()
            return dict(user)

def get_user_by_id(user_id):
    query = "SELECT id, google_id, email, username, avatar_url, created_at, last_login FROM users WHERE id = %s;"
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (user_id,))
            user = cur.fetchone()
            return dict(user) if user else None
