import os
import sqlite3
from datetime import date, datetime, timedelta

from kivy.app import App

DB_NAME = os.path.join(os.path.dirname(__file__), "database.db")


def conectar():
    return sqlite3.connect(DB_NAME)


def create_pontos_table():
    conn = conectar()
    cursor = conn.cursor()
  
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pontos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            dia TEXT NOT NULL,
            dia_semana TEXT NOT NULL,
            entrada TEXT NOT NULL,
            intervalo TEXT NOT NULL,
            retorno TEXT NOT NULL,
            saida TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    criar_dados_exemplo()
    conn.commit()
    conn.close()


def inserir_ponto(user_id, dia, dia_semana, entrada, intervalo, retorno, saida):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pontos (user_id, dia, dia_semana, entrada, intervalo, retorno, saida)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, dia, dia_semana, entrada, intervalo, retorno, saida))

    
    conn.commit()
    conn.close()


def listar_pontos():
    conn = conectar()
    cursor = conn.cursor()

    app = App.get_running_app()
    cursor.execute(
        "SELECT * FROM pontos WHERE user_id = ? ORDER BY id DESC",
        (app.user_id,)
    )
    dados = cursor.fetchall()

    conn.close()
    return dados

def buscar_pontos_mes(ano, mes):
    con = conectar()
    cur = con.cursor()
    app = App.get_running_app()
   

    padrao = f"%/{mes}/{ano}"

    cur.execute("""
        SELECT * FROM pontos
        WHERE dia LIKE ? AND user_id = ?
        ORDER BY dia DESC
    """, (padrao, app.user_id))
    dados = cur.fetchall()

    con.close()
    return dados


def buscar_ontem():
    con = conectar()
    cur = con.cursor()

    app = App.get_running_app()

    ontem = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")

    cur.execute("""
        SELECT dia, dia_semana, entrada, intervalo, retorno, saida
        FROM pontos
        WHERE dia = ? AND user_id = ?
    """, (ontem, app.user_id))

    dados = cur.fetchall()
    con.close()
    return dados

def buscar_semana():
    con = conectar()
    cur = con.cursor()

    app = App.get_running_app()

    hoje = date.today()
    sete_dias_atras = hoje - timedelta(days=6)

    hoje_str = hoje.strftime("%d/%m/%Y")
    inicio_str = sete_dias_atras.strftime("%d/%m/%Y")     # domingo

    cur.execute("""
        SELECT * FROM pontos
        WHERE user_id = ?
        AND dia BETWEEN ? AND ?
        ORDER BY dia DESC
    """, (app.user_id, inicio_str, hoje_str))

    dados = cur.fetchall()

    con.close()
    return dados

def criar_dados_exemplo():
    """Cria 5 pontos apenas se a tabela estiver vazia."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM pontos")
    total = cursor.fetchone()[0]

    if total == 0:
        exemplos = [
            (1, "20/11/2025", "Quinta", "08:00", "12:00", "13:00", "17:00"),
            (1, "21/11/2025", "Sexta", "08:10", "12:05", "13:00", "17:10"),
            (1, "22/11/2025", "Sábado", "09:00", "12:00", "13:30", "16:00"),
            (1, "23/11/2025", "Domingo", "10:00", "12:00", "13:00", "15:00"),
            (1, "24/11/2025", "Segunda", "07:55", "12:00", "13:00", "17:05"),
        ]

        cursor.executemany("""
            INSERT INTO pontos (user_id, dia, dia_semana, entrada, intervalo, retorno, saida)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, exemplos)

        conn.commit()
        print("Pontos inseridos com sucesso.")

    conn.close()


def verificar_ponto_no_dia(dia):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    app = App.get_running_app()
    user_id = app.user_id
    cursor.execute("SELECT COUNT(*) FROM pontos WHERE dia = ? AND user_id = ?", (dia,user_id))
    total = cursor.fetchone()[0]

    conn.close()
    return total > 0
