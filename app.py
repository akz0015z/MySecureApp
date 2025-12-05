from flask import Flask, request, render_template, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "123"   # this is a insecure hardcoded weak secret key example

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# this is where we running the database

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


# this is the insecure version of registration

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]  # password stored in plaintext

        # this is the insecure sql injection
        conn = get_db()
        conn.execute(f"INSERT INTO users (username, email, password, bio) VALUES ('{username}', '{email}', '{password}', '')")
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# this is the insecure login and reflected xss

@app.route("/login", methods=["GET", "POST"])
def login():
    error = request.args.get("error", "")

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        # this is the insecure sql injection login
        query = f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'"
        print("INSECURE SQL QUERY:", query)  

        user = conn.execute(query).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            return redirect("/profile")
        else:
            # REFLECTED XSS
            return redirect("/login?error=Invalid+login:+" + email)

    return render_template("login.html", error=error)



# this is the stored xss vulnreability profile 

@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    user = conn.execute(f"SELECT * FROM users WHERE id={session['user_id']}").fetchone()
    conn.close()

    return render_template("profile.html", user=user)


# this is the edit profile (stored XSS injection point)

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


# where we run app

if __name__ == "__main__":
    app.run(debug=True)
