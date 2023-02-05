from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("social_media.db")
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        conn.close()

        return render_template("dashboard.html", user=username)
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user is not None:
            return render_template("dashboard.html", user=username)
        else:
            return "Incorrect username or password"
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    user = request.form["user"]

    if request.method == "POST":
        text = request.form["text"]

        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO posts (user, text) VALUES (?, ?)", (user, text))
        conn.commit()
        conn.close()

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM posts")
    posts = c.fetchall()
    conn.close()

    return render_template("dashboard.html", user=user, posts=posts)

if __name__ == "__main__":
    conn = get_db()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username text, password text, email text)")
    c.execute("CREATE TABLE IF NOT EXISTS posts (user text, text text)")
    conn.commit()
    conn.close()
    app.run()
