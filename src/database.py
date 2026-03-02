import sqlite3
import os

# Define o caminho do BD na pasta 'data'
DB_PATH = "data/preços.db"

def setup_database():
    """
    Cria as tabelas no banco de dados SQLite caso elas não existam.
    """

    # Garante que a pasta 'data' existe antes de criar o arquico .db
    os.makedirs(os.path.dirname(DB_PATH), exist_ok = True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabela 1: Produtos (Dados fixos que não mudam)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT ,
            url TEXT UNIQUE NOT NULL,
            titulo TEXT NOT NULL
        )
    ''')

    # Tabela 2 : Histórico de Preços (Dados que mudam com o tempo)
    # Tem uma Chave_Estrangeira (produto_id) que liga com a tabela produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_precos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            preco REAL NOT NULL,
            data_hora TEXT NOT NULL,
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Banco de Dados configurado com sucesso! ")

def save_data(dados):
    """
    Recebe o dicionario de dados do scraper e salva no banco de dados.
    Verifica se o produto ja existe para não duplicar na tabela 'produtos'
    """
    if not dados:
        print("Nenhum dado para salvar.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 1. Tenta inserir o produto na tabela 'produtos'
        # O "OR IGNORE" evita erro se a url já estiver cadastrada (pois a URL é UNIQUE)
        cursor.execute('''
            INSERT OR IGNORE INTO produtos (url, titulo)
            VALUES (?, ?)
        ''', (dados['url'], dados['Produto']))
        
        # 2. Descobre qual é o ID do produto (seja ele novo ou já existente)
        cursor.execute('SELECT id FROM produtos WHERE url = ?', (dados['url'],))
        produto_id = cursor.fetchone()[0]

        # 3. Insere o preço de hoje na tabela 'historico_precos' associado a esse ID
        cursor.execute('''
            INSERT INTO historico_precos (produto_id, preco, data_hora)
            VALUES (?, ?, ?)
        ''', (produto_id, dados['preco'], dados['data_hora']))

        conn.commit()
        print(f" Preço de R$ {dados['preco']} salvo para o produto ID {produto_id}.")

    except sqlite3.Error as e:
        print(f" Erro ao salvar no banco de dados: {e}")

    finally:
        conn.close()

# Bloco de execução para testar a criação de tabelas
if __name__ == "__main__":
    print("Iniciando setup do banco de dados ...")
    setup_database()