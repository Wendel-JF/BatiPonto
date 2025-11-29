import os
import sqlite3

import bcrypt
from kivymd.toast import toast

DB_NAME = os.path.join(os.path.dirname(__file__), "database.db")


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)

    email = "user@teste.com"
    # Criar usuário padrão se não existir
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    exists = cursor.fetchone()

    if not exists:
        password_hash = bcrypt.hashpw("123".encode(), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO users (email, name, password) VALUES (?, ?, ?)",
            (email, "Bruno", password_hash)
        )

    conn.commit()
    conn.close()


def verify_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, email, password FROM users WHERE email=?", (email,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    user_id, email, hashed = row

    if bcrypt.checkpw(password.encode(), hashed):
        return {"id": user_id, "email": email}

    return None


def registrar_usuario(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    exists = cursor.fetchone()

   
    if exists:
        print("Usuário já existe!")
        toast("Usuário já existe!")
        conn.close()
        return
    
    
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cursor.execute("""
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
        """, (name, email, password_hash))
        conn.commit()
        print("Usuário cadastrado com sucesso!")
        toast("Cadastro realizado com sucesso!")
    except sqlite3.IntegrityError as e:
        print("Erro:", e)

    conn.close()


def get_user_data(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM users WHERE id = ?", (user_id,))
    
    return cursor.fetchone()