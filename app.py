from flask import Flask, request, render_template, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "123"   # INSECURE: hardcoded weak secret key

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ------------------------------------
# Initialize DB (Run once)
# ------------------------------------
def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            password TEXT,     -- INSECURE: plaintext password
            bio TEXT           -- INSECURE: stored XSS
        );
    """)

    conn.commit()
    conn.close()

init_db()

# ------------------------------------
# Register (INSECURE)
# ------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]  # stored in plaintext

        # INSECURE: SQL Injection vulnerability
        conn = get_db()
        conn.execute(f"INSERT INTO users (username, email, password, bio) VALUES ('{username}', '{email}', '{password}', '')")
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# ------------------------------------
# Login (INSECURE + Reflected XSS)
# ------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = request.args.get("error", "")

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        # INSECURE SQL INJECTION LOGIN
        query = f"SELECT * FROM users WHERE email='{email}' AND password='{password}'"
        user = conn.execute(query).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            return redirect("/profile")
        else:
            # Reflected XSS
            return redirect("/login?error=Invalid+login:+"+email)

    return render_template("login.html", error=error)

# ------------------------------------
# Profile (Stored XSS Vulnerability)
# ------------------------------------
@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    user = conn.execute(f"SELECT * FROM users WHERE id={session['user_id']}").fetchone()
    conn.close()

    return render_template("profile.html", user=user)

# ------------------------------------
# Edit Profile (Stored XSS Injection Point)
# ------------------------------------
@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        bio = request.form["bio"]  # INSECURE

        conn = get_db()
        conn.execute(f"UPDATE users SET bio='{bio}' WHERE id={session['user_id']}")
        conn.commit()
        conn.close()

        return redirect("/profile")

    return render_template("edit_profile.html")

# ------------------------------------
# Run app
# ------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
