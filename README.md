# 🛠 Mini Sentrix - Sistema de Gestión de Incidentes con IA

Aplicación web para registrar y gestionar incidentes IT con clasificación automática utilizando inteligencia artificial local.

---

## 🚀 Features

- Alta de incidentes
- Gestión de estados (abierto, en proceso, cerrado)
- Clasificación automática con IA (tipo y prioridad)
- Motor de IA local usando LM Studio (sin costo)
- Reglas adicionales para mejorar consistencia
- Interfaz simple con colores por prioridad

---

## 🧠 Tecnologías

- Python
- Flask
- SQLite
- LM Studio (LLM local)
- Modelo: Phi-3 Mini

---

## 🤖 IA

El sistema utiliza un modelo local (Phi-3 Mini) ejecutado vía LM Studio, utilizando una API compatible con OpenAI.

Se aplica:

- Prompt engineering
- Respuesta estructurada en JSON
- Validación mediante reglas propias

---

## ⚙️ Instalación

```bash
git clone https://github.com/awmorante/mini-sentrix.git
cd mini-sentrix
pip install -r requirements.txt
python app.py