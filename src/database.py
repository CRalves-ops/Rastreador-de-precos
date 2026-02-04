import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

# 1. Configuração do Banco de Dados

# Define onde o arquivo .db será salvo (pasta 'data')
DB_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
DB_PATH = os.path.join(DB_FOLDER, 'preços.db')

# Cria a pasta 'data' se ela não existir (segurança contra erros)
os.makedirs(DB_FOLDER, exist_ok=True)

# Cria a conexão com o banco SQLite
engine = create_engine(f'sqlite:///{DB_PATH}', echo= False)

# Base para os modelos (tabelas)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# 2. Definição das Tabelas (Modelos)

class Produto(Base):
    """
    Tabela que armazena os produtos monitorados.
    Evita repetição de dados estáticos como nome e link.
    """
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key = True)
    nome = Column(String, nullable = False)
    url = Column(String, unique = True, nullable = False) # URL única para não duplicar
    loja = Column(String) # EX: Amazon, Mercado Livre
    criado_em = Column(DateTime, default = datetime.now)

    # Relacionamento: Um produto tem muitos preços
    precos = relationship("Historico_preco", back_populates = "Produtos", cascade= "all, delete-orphan")

    def __repr__(self):
        return f"<Produto( nome = '{self.nome}', loja = '{self.loja}')>"
    
class PrecoHistorico(Base):
    """
    Tabela que armazena o histórico de preços.
    Cada linha é um 'snapshot' do preço em um momento específico.
    """
    __tablename__ = 'Historico_preco'

    id = Column(Integer, primary_key = True)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable = False) # Chave Estrangeira
    preco = Column(Float, nullable = False)
    data_raspagem = Column(DateTime, default = datetime.now)

    # Relacionamento Inverso
    produto = relationship("produto", back_populates= "precos")

    def __repr__(self):
        return f"<Preço( valor = '{self.preco}', data = '{self.data_raspagem}')>"
    
# 3. Função para Inicializar o Banco
def init_db():
    """
    Cria as tabelas no banco de dados se elas não existirem.
    """
    Base.metadata.create_all(engine)
    print(f"Banco de dados inicializado com sucesso em: {DB_PATH}")

# Bloco de execução direta (para testar o arquivo)
if __name__ == "__main__":
    init_db()