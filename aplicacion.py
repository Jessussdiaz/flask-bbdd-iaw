from flask import Flask, render_template, request, redirect, url_for, abort
import sqlite3
# Autores: Alejandro Luna Paredes y Jesús Díaz Mata
# Fecha 03/12/2025

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('coches.db')
    conn.row_factory = sqlite3.Row
    return conn


# --------------------------------------------------
# HOME
# --------------------------------------------------
@app.route("/")
def home():
    entidades = [
        {
            "titulo": "Marcas",
            "descripcion": "Listado de marcas de vehículos.",
            "endpoint": "lista_marcas",
        },
        {
            "titulo": "Vehículos",
            "descripcion": "Listado completo de vehículos.",
            "endpoint": "lista_coches",
        },
    ]
    return render_template("home.html", entidades=entidades)


# --------------------------------------------------
# LISTADO MARCAS
# --------------------------------------------------
@app.route("/marcas/")
def lista_marcas():
    db = get_db_connection()
    marcas = db.execute("""
        SELECT m.id,
               m.nombre,
               m.pais,
               m.anio_fundacion,
               COUNT(c.id) AS num_modelos
        FROM marcas m
        LEFT JOIN coches c ON c.id_marca = m.id
        GROUP BY m.id, m.nombre, m.pais, m.anio_fundacion
        ORDER BY m.nombre
    """).fetchall()
    db.close()
    return render_template("marcas.html", marcas=marcas)


# --------------------------------------------------
# LISTADO COCHES (para coches.html)
# --------------------------------------------------
@app.route("/coches/")
def lista_coches():
    conn = get_db_connection()
    coches = conn.execute("""
        SELECT c.id,
               c.modelo,
               c.anio,
               c.tipo_motor,
               c.potencia,
               m.nombre AS marca
        FROM coches c
        LEFT JOIN marcas m ON m.id = c.id_marca
        ORDER BY c.id, marca, modelo
    """).fetchall()
    conn.close()
    return render_template("coches.html", coches=coches)


# --------------------------------------------------
# DETALLE MARCA (coches de esa marca)
# --------------------------------------------------
@app.route('/marca/<int:marca_id>')
def detalle_marca(marca_id):
    conn = get_db_connection()
    marca = conn.execute(
        "SELECT * FROM marcas WHERE id = ?",
        (marca_id,)
    ).fetchone()

    if marca is None:
        conn.close()
        abort(404)

    modelos = conn.execute(
        "SELECT * FROM coches WHERE id_marca = ? ORDER BY modelo",
        (marca_id,)
    ).fetchall()

    conn.close()
    return render_template("detalle_marca.html", marca=marca, modelos=modelos)


# --------------------------------------------------
# EDITAR MARCA
# --------------------------------------------------
@app.route("/marca/<int:marca_id>/editar", methods=["GET", "POST"])
def editar_marca(marca_id):
    conn = get_db_connection()
    marca = conn.execute(
        "SELECT * FROM marcas WHERE id = ?",
        (marca_id,)
    ).fetchone()

    if marca is None:
        conn.close()
        abort(404)

    if request.method == "POST":
        nombre = request.form["nombre"]
        pais = request.form["pais"]
        anio_fundacion = request.form["anio_fundacion"]
        fundador = request.form["fundador"]

        conn.execute(
            "UPDATE marcas SET nombre = ?, pais = ?, anio_fundacion = ?, fundador = ? WHERE id = ?",
            (nombre, pais, anio_fundacion, fundador, marca_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("detalle_marca", marca_id=marca_id))

    conn.close()
    return render_template("editar_marca.html", marca=marca)


# --------------------------------------------------
# EDITAR COCHE
# --------------------------------------------------
@app.route("/coche/<int:coche_id>/editar", methods=["GET", "POST"])
def editar_coche(coche_id):
    conn = get_db_connection()
    coche = conn.execute(
        "SELECT * FROM coches WHERE id = ?",
        (coche_id,)
    ).fetchone()

    if coche is None:
        conn.close()
        abort(404)

    if request.method == "POST":
        modelo = request.form["modelo"]
        anio = request.form["anio"]
        tipo_motor = request.form["tipo_motor"]
        potencia = request.form["potencia"]

        conn.execute("""
            UPDATE coches
            SET modelo = ?, anio = ?, tipo_motor = ?, potencia = ?
            WHERE id = ?
        """, (modelo, anio, tipo_motor, potencia, coche_id))

        conn.commit()
        id_marca = coche["id_marca"]  # para volver al detalle de su marca
        conn.close()
        return redirect(url_for("detalle_marca", marca_id=id_marca))

    conn.close()
    return render_template("editar_coche.html", coche=coche)


# --------------------------------------------------
# BORRAR MARCA
# --------------------------------------------------
@app.route("/marca/<int:marca_id>/borrar", methods=["GET", "POST"])
def borrar_marca(marca_id):
    conn = get_db_connection()
    
    # Obtener la marca
    marca = conn.execute(
        "SELECT * FROM marcas WHERE id = ?",
        (marca_id,)
    ).fetchone()
    
    if marca is None:
        conn.close()
        abort(404)

    # Contar cuántos coches tiene la marca
    total_coches = conn.execute(
        "SELECT COUNT(*) AS total FROM coches WHERE id_marca = ?",
        (marca_id,)
    ).fetchone()["total"]

    if request.method == "POST":
        # Borrar coches y marca
        conn.execute("DELETE FROM coches WHERE id_marca = ?", (marca_id,))
        conn.execute("DELETE FROM marcas WHERE id = ?", (marca_id,))
        conn.commit()
        conn.close()
        return redirect(url_for("lista_marcas"))

    conn.close()
    return render_template("borrar_marca.html", marca=marca, total_coches=total_coches)

@app.route("/añadirmarca/", methods=["GET", "POST"])
def añadirmarca():
    if request.method == "POST":
        nombre = request.form["nombre"]
        pais = request.form["pais"]
        fundador = request.form["fundador"]
        anio_fundacion = request.form["anio_fundacion"]
    
        conn = get_db_connection()
        marca = conn.execute("INSERT INTO marcas (nombre, pais, fundador, anio_fundacion) VALUES (?, ?, ?, ?)",
                                (nombre, pais, fundador, anio_fundacion))
        conn.commit()
        conn.close()
        return redirect(url_for("lista_marcas"))
        

    return render_template("añadirmarca.html")


@app.route("/añadircoche/", methods=["GET", "POST"])
def añadircoche():
    conn = get_db_connection()
    
    if request.method == "POST":
        modelo = request.form["modelo"]
        id_marca = request.form["id_marca"]
        anio = request.form["anio"]
        tipo_motor = request.form["tipo_motor"]
        potencia = request.form["potencia"]
    
        conn.execute("""
            INSERT INTO coches (modelo, id_marca, anio, tipo_motor, potencia) 
            VALUES (?, ?, ?, ?, ?)
        """, (modelo, id_marca, anio, tipo_motor, potencia))
        
        conn.commit()
        conn.close()
        return redirect(url_for("lista_coches"))

    # Para el GET: Obtenemos las marcas para el menú desplegable
    marcas = conn.execute("SELECT id, nombre FROM marcas ORDER BY nombre").fetchall()
    conn.close()
    return render_template("añadircoche.html", marcas=marcas)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
