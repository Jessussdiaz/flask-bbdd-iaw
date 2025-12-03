import sqlite3

# Conexión a la base de datos
connection = sqlite3.connect('coches.db')

# Ejecutar script SQL con las tablas (marcas y coches)
with open('coches.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# ===========================
# INSERTS PARA TABLA MARCAS
# ===========================
cur.execute("""
INSERT INTO marcas (id, nombre, pais, fundador, anio_fundacion)
VALUES (1, 'Toyota', 'Japón', 'Kiichiro Toyoda', 1937)
""")

cur.execute("""
INSERT INTO marcas (id, nombre, pais, fundador, anio_fundacion)
VALUES (2, 'Ford', 'Estados Unidos', 'Henry Ford', 1903)
""")

cur.execute("""
INSERT INTO marcas (id, nombre, pais, fundador, anio_fundacion)
VALUES (3, 'BMW', 'Alemania', 'Karl Rapp', 1916)
""")

# ===========================
# INSERTS PARA TABLA COCHES
# ===========================
cur.execute("""
INSERT INTO coches (id, modelo, id_marca, anio, tipo_motor, potencia)
VALUES (1, 'Corolla', 1, 2020, 'Gasolina', 132)
""")

cur.execute("""
INSERT INTO coches (id, modelo, id_marca, anio, tipo_motor, potencia)
VALUES (2, 'Mustang', 2, 2019, 'Gasolina', 450)
""")

cur.execute("""
INSERT INTO coches (id, modelo, id_marca, anio, tipo_motor, potencia)
VALUES (3, 'M3', 3, 2021, 'Gasolina', 480)
""")

connection.commit()
connection.close()
