import os
import sqlite3

DB_NAME = os.path.join(os.path.dirname(__file__), "database.db")


def conectar():
    return sqlite3.connect(DB_NAME)


def create_pontos_table():
    conn = conectar()
    cursor = conn.cursor()
    # ativar foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pontos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER,
            dia TEXT NOT NULL,
            dia_semana TEXT NOT NULL,
            entrada TEXT NOT NULL,
            intervalo TEXT NOT NULL,
            retorno TEXT NOT NULL,
            saida TEXT NOT NULL,
            FOREIGN KEY (id_user) REFERENCES users(id)
        )
    """)

    criar_dados_exemplo()
    conn.commit()
    conn.close()


def inserir_ponto(id_user, dia, dia_semana, entrada, intervalo, retorno, saida):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pontos (id_user, dia, dia_semana, entrada, intervalo, retorno, saida)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (id_user, dia, dia_semana, entrada, intervalo, retorno, saida))

    
    conn.commit()
    conn.close()


def listar_pontos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pontos ORDER BY id DESC")
    dados = cursor.fetchall()

    conn.close()
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
            INSERT INTO pontos (id_user, dia, dia_semana, entrada, intervalo, retorno, saida)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, exemplos)

        conn.commit()
        print("Pontos inseridos com sucesso.")

    conn.close()


def verificar_ponto_no_dia(dia):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM pontos WHERE dia = ?", (dia,))
    total = cursor.fetchone()[0]

    conn.close()
    return total > 0
