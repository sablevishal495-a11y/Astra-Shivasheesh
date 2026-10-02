import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from db import init_db, upsert_google_user, get_user_by_id
load_dotenv()

app = Flask(__name__)
raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5500,http://127.0.0.1:5500,http://localhost:3000")
allowed_origins = [o.strip() for o in raw_origins.split(",") if o.strip()]
CORS(app, resources={r"/api/*": {"origins": allowed_origins}})

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

# Initialize database schema on startup
db_ok, db_msg = init_db()
if not db_ok:
    print(f"[WARN] Database initialization notice: {db_msg}")

@app.route("/api/health", methods=["GET"])
def health():
    ok, msg = init_db()
    return jsonify({
        "status": "online",
        "database": "connected" if ok else "disconnected",
        "database_message": msg
    })

@app.route("/api/auth/google", methods=["POST"])
def google_auth():
    if not request.is_json:
        return jsonify({"success": False, "message": "Content-Type must be application/json"}), 415

    data = request.get_json(silent=True) or {}
    credential = data.get("credential")

    if not credential:
        return jsonify({"success": False, "message": "Missing Google credential token"}), 400

    try:
        # Verify token with Google's public OAuth2 verification endpoint
        verify_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={credential}"
        resp = requests.get(verify_url, timeout=5)

        if resp.status_code != 200:
            return jsonify({"success": False, "message": "Invalid Google credential"}), 401

        token_info = resp.json()

        # If GOOGLE_CLIENT_ID is configured, verify audience matches
        if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_ID != "your-google-client-id.apps.googleusercontent.com":
            if token_info.get("aud") != GOOGLE_CLIENT_ID:
                return jsonify({"success": False, "message": "Token audience does not match configured CLIENT_ID"}), 403

        # Extract user profile from token
        google_id = token_info.get("sub")
        email = token_info.get("email")
        name = token_info.get("name", email.split("@")[0] if email else "Astra User")
        picture = token_info.get("picture", "")

        # Persist to PostgreSQL database
        user = upsert_google_user(
            google_id=google_id,
            email=email,
            username=name,
            avatar_url=picture
        )

        # Convert timestamps to ISO format for JSON serialization
        if "created_at" in user and user["created_at"]:
            user["created_at"] = user["created_at"].isoformat()
        if "last_login" in user and user["last_login"]:
            user["last_login"] = user["last_login"].isoformat()

        return jsonify({
            "success": True,
            "user": user,
            "token": credential
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Authentication failed: {str(e)}"}), 500

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 5001))
    print(f"ASTRA Backend running on http://{host}:{port}")
    app.run(host=host, port=port, debug=False)

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("../", filename)