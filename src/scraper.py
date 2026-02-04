import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs
from datetime import datetime

# Importação condiconal para funcionar tanto rodando sa raiz quanto da pasta src
try:
    from src.database import Session, Produto, PrecoHistorico

except ModuleNotFoundError:
    from database import Session, Produto, PrecoHistorico

# Configuração de logs
logging.basicConfig(level= logging.INFO, format= '%(asctime)s - %(levelname)s - %(message)s') 

def setup_driver():
    """Configura o navegador Chrome Headless"""
    chrome_options = Options()

    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service()  # Selenium Manager
    return webdriver.Chrome(service=service, options=chrome_options)

def get_info_produto(url):
    """
    Acessa o site e retorna um dicionario com nome e preço.
    """
    driver = setup_driver()

    try:
        logging.info(f"Acessando: {url}")
        driver.get(url)
        time.sleep(3) # Espera carregar os scripts sinâmicos

        soup = bs(driver.page_source, 'html.parser')
        
        # 1. Extração do Título (Geralmente h1 nos sites de e-commerce)
        titulo_tag = soup.find('h1')
        produto_nome = titulo_tag.get_text().strip() if titulo_tag else "Nome desconhecido"

        # 2. Extração do Preço (Meta tag mais confiável no ML)
        preco_tag = soup.find('meta', {'itemprop': 'price'})
        if preco_tag:
            preco = float(preco_tag['content'])
            return {
                'nome': produto_nome,
                'preço': preco,
                'url': url,
                'loja': 'Mercado Livre' # Por enquanto somente mercado livre
            }
        else:
            logging.error("Preço não encontrado.")
            return None
        
    except Exception as e:
        logging.error(f"Erro na extração: {e}")
        return None
    finally:
        driver.quit()

def save_to_db(data):
    """
    Recebe um dicionario de dados e salva no banco de dados SQLite.
    Usa a lógica de Upset (Update ou Insert).
    """
    if not data:
        return
    
    session = Session()
    try:
        # 1. Verifica se o produto já existe no banco (pela url)
        produto = session.query(Produto).filter_by(url = data['url']).first()

        # 2. Se não existir, cria um novo produto
        if not produto:
            logging.info(f"Novo produto detectado: {data['nome']}")
            produto = Produto(
                nome = data['nome'],
                url = data['url'],
                loja = data['loja']
            )
            session.add(produto)
            session.commit() # Commit necessário para gerar o ID do produto
        else:
            logging.info(f"Produto já monitorado: {produto.nome}")

        # 3, Adiciona o novo registro de preço no historico
        novo_preco = PrecoHistorico(
            produto_id = produto.id,
            preco = data['preço'],
            data_raspagem = datetime.now()
        )
        session.add(novo_preco)
        session.commit()
        logging.info(f"Preço atualizado: R$ {data['preço']}")

    except Exception as e:
        logging.error(f"Erro ao salvar no banco: {e}")
        session.rollback()

    finally:
        session.close()

# Bloco de execução principal
if __name__ == '__main__':
    # Lista de URls para testar
    urls_para_monitorar = [
        "https://produto.mercadolivre.com.br/MLB-5936349344-kit-2-controle-ps2-compativel-joystick-analogico-vibraco-_JM#polycard_client=recommendations_pdp-v2p&reco_backend=ranker_retrieval_online_vpp_v2p&reco_model=coldstart_high_exposition&reco_client=pdp-v2p&reco_item_pos=0&reco_backend_type=low_level&reco_id=10f2249f-d57c-4062-89e9-eee34b5f02bc&wid=MLB5936349344&sid=recos"
    ]

    print("--- Iniciando Coleta ---")
    for url in urls_para_monitorar:
        info = get_info_produto(url)
        if info:
            save_to_db(info)

    print("--- Coleta finalizada ---")