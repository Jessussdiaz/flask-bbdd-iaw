# Práctica Flask + SQLite3 — Implantación de Aplicaciones Web (IAW)

Este repositorio contiene el desarrollo completo de la práctica de la asignatura **Implantación de Aplicaciones Web (IAW)**.  
El objetivo es crear una **aplicación web en Flask** con acceso a datos mediante **SQLite3**, cumpliendo todos los requisitos establecidos: integridad referencial, claves primarias y foráneas, CRUD completo y gestión de dos entidades relacionadas.

---

## Objetivos del proyecto

La aplicación implementa:

- Almacenamiento en **SQLite3** con integridad referencial.
- Una **entidad principal** y una **entidad relacionada** mediante clave foránea.
- CRUD completo (Create, Read, Update, Delete) sobre cada entidad.
- Páginas dedicadas para:
  - Listado  
  - Consulta  
  - Altas  
  - Modificaciones  
  - Bajas  
- Uso de botones *Glyphicons* (o equivalentes) para acciones rápidas.
- Validación de claves foráneas mediante desplegables.
- Redirecciones y mensajes de confirmación para evitar borrados indebidos.

---

## Base de Datos (SQLite3)

- Se utiliza **SQLite3** como motor principal.
- Cada tabla tiene:
  - `id` como clave primaria.
  - Al menos **4 campos adicionales**.
  - Una clave única independiente.
- La entidad secundaria tiene una **clave foránea** que apunta a la entidad principal.
- La relación está definida con:
  
```sql
FOREIGN KEY(id_entidad_principal) REFERENCES entidad(id) ON DELETE RESTRICT
