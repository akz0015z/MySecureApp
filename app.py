from flask import Flask, request, render_template, redirect, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from flask_bcrypt import Bcrypt
from flask_talisman import Talisman
import sqlite3
import logging
import os


# My App


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)        # This is the secure version with strong random secret key
bcrypt = Bcrypt(app)

# the security headers
Talisman(app, content_security_policy={
    "default-src": ["'self'"],
    "style-src": ["'self'", "'unsafe-inline'"],
})


# The logging part


if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)


# the database


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT UNIQUE,
            password TEXT,
            bio TEXT
        );
    """)

    conn.commit()
    conn.close()

init_db()


# the homepage redirect to login


@app.route("/")
def home():
    return redirect("/login")



# the csrf protected coding


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class EditProfileForm(FlaskForm):
    bio = TextAreaField("Bio", validators=[Length(max=300)])



# app's routes


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data).decode()

        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users (username, email, password, bio) VALUES (?, ?, ?, ?)",
                (username, email, password, "")
            )
            conn.commit()
            logging.info(f"New user registered: {email}")

            return redirect("/login")

        except sqlite3.IntegrityError:
            flash("Email already exists", "error")

        conn.close()

    return render_template("register.html", form=form)



@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user["password"], password):
            session.clear()
            session["user_id"] = user["id"]

            logging.info(f"User logged in: {email}")
            return redirect("/profile")
        else:
            flash("Invalid login credentials", "error")

    return render_template("login.html", form=form)



@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    conn.close()

    return render_template("profile.html", user=user)



@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    if "user_id" not in session:
        return redirect("/login")

    form = EditProfileForm()

    if form.validate_on_submit():
        bio = form.bio.data.strip()

        # VALIDATION: prevent empty bio
        if bio == "":
            flash("Bio cannot be empty", "error")
            return redirect("/edit_profile")

        conn = get_db()
        conn.execute("UPDATE users SET bio = ? WHERE id = ?", (bio, session["user_id"]))
        conn.commit()
        conn.close()

        flash("Profile updated!", "success")
        return redirect("/profile")

    return render_template("edit_profile.html", form=form)



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")



# starting the app


if __name__ == "__main__":
    app.run(debug=True)
