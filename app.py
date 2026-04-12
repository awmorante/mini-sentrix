from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

@app.route("/")
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents")
    incidents = cursor.fetchall()
    conn.close()
    return render_template("index.html", incidents=incidents)

@app.route("/add", methods=["POST"])
def add_incident():
    title = request.form["title"]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO incidents (title, status) VALUES (?, ?)", (title, "abierto"))
    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)