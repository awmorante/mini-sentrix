from flask import Flask, render_template, request, redirect
import sqlite3
import requests

API_KEY = ""

def clasificar_incidente(texto):
    texto = texto.lower()

    if "sql" in texto or "db" in texto:
        return "tipo: base de datos | prioridad: alta"
    elif "red" in texto or "internet" in texto:
        return "tipo: red | prioridad: media"
    elif "server" in texto or "servidor" in texto:
        return "tipo: servidor | prioridad: alta"
    else:
        return "tipo: otro | prioridad: baja"
    
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

    clasificacion = clasificar_incidente(title)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO incidents (title, status) VALUES (?, ?)",
        (f"{title} | {clasificacion}", "abierto")
    )
    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)