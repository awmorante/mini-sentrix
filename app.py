from flask import Flask, render_template, request, redirect
import sqlite3
import requests
import json

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

def clasificar_incidente(texto):
    prompt = f"""
    Clasificá este incidente IT en:
    tipo (red, servidor, base de datos, hardware, otro)
    prioridad (baja, media, alta)

    Incidente: {texto}

    Respondé SOLO en JSON válido así:

    {{
      "tipo": "red | servidor | base de datos | hardware | otro",
      "prioridad": "baja | media | alta"
    }}
    """

    response = requests.post(
        "http://localhost:1234/v1/chat/completions",
        json={
            "model": "phi-3-mini-128k-instruct-imatrix-smashed",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
    )

    data = response.json()
    texto_respuesta = data["choices"][0]["message"]["content"]

    # 🔥 PARSEO PRO
    try:
        resultado = json.loads(texto_respuesta)
        tipo = resultado.get("tipo", "otro")
        prioridad = resultado.get("prioridad", "baja")
    except:
        tipo = "otro"
        prioridad = "baja"

    return tipo, prioridad

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