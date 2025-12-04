from flask import Flask, render_template, request, redirect, url_for
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

@app.route("/coches/")
def coches():
    db = get_db_connection()
    coches = db.execute("SELECT * FROM coches").fetchall()
    if coches is None:
        return redirect(url_for("home"))
    return render_template("coches.html", coches=coches)


@app.route("/marcas/")
def marcas():
    db = get_db_connection()
    marcas = db.execute("SELECT * FROM marcas").fetchall()
    if marcas is None:
        return redirect(url_for("home"))
    return render_template("marcas.html", marcas=marcas)


app.run(host="0.0.0.0", port=5000, debug=True)