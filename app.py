from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

# 🔥 CLASIFICACIÓN BIEN HECHA
def clasificar_incidente(texto):
    texto = texto.lower()

    if "sql" in texto or "db" in texto or "base de datos" in texto:
        return "base de datos", "alta"
    elif "red" in texto or "internet" in texto:
        return "red", "media"
    elif "server" in texto or "servidor" in texto:
        return "servidor", "alta"
    else:
        return "otro", "baja"

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

    tipo, prioridad = clasificar_incidente(title)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO incidents (title, status, tipo, prioridad) VALUES (?, ?, ?, ?)",
        (title, "abierto", tipo, prioridad)
    )
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/update/<int:id>/<status>")
def update_status(id, status):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE incidents SET status=? WHERE id=?", (status, id))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)