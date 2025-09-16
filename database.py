import sqlite3

# Conectar (ou criar) banco de dados chamado 'usuarios.db'
conn = sqlite3.connect('usuarios.db')

# Criar cursor para executar comandos SQL
cursor = conn.cursor()

# Criar tabela 'usuarios' com colunas id, nome, email e idade
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    idade INTEGER
)
''')

# Inserir usuários de exemplo
usuarios_exemplo = [
    ('Alice Silva', 'alice@example.com', 28),
    ('Bruno Costa', 'bruno@example.com', 34),
    ('Carla Souza', 'carla@example.com', 22),
]

cursor.executemany('''
INSERT INTO usuarios (nome, email, idade) VALUES (?, ?, ?)
''', usuarios_exemplo)

# Salvar as alterações
conn.commit()

# Consultar todos os usuários
cursor.execute('SELECT * FROM usuarios')
usuarios = cursor.fetchall()

# Mostrar os usuários cadastrados
for usuario in usuarios:
    print(usuario)

# Fechar a conexão
conn.close()
