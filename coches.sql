CREATE TABLE marcas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    pais TEXT NOT NULL,
    fundador TEXT NOT NULL,
    anio_fundacion INTEGER NOT NULL
);

CREATE TABLE coches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modelo TEXT UNIQUE NOT NULL,
    id_marca INTEGER NOT NULL,
    anio INTEGER NOT NULL,
    tipo_motor TEXT NOT NULL,
    potencia INTEGER NOT NULL,
    FOREIGN KEY (id_marca) REFERENCES marcas(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);
