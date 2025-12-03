from flask import Flask, render_template, request, redirect, url_for
import sqlite3
# Autores: Alejandro Luna Paredes y Jesús Díaz Mata
# Fecha 03/12/2025

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('coches.db')
    conn.row_factory = sqlite3.Row
    return conn