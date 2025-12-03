from flask import Flask, render_template
import sqlite3
# Autores: Alejandro Luna Paredes y Jesús Díaz Mata
# Fecha 03/12/2025

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('coches.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    entidades = conn.execute("""
    SELECT name FROM sqlite_master 
    WHERE type='table' AND name NOT LIKE 'sqlite_%';
""").fetchall()
    conn.close()
    return render_template('home.html', entidades=entidades)

app.run(debug=True)
