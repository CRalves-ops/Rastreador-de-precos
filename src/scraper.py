import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database import setup_database, save_data

def get_produto_data(url):
    """
    Acessa a página de um produto do Mercado Livre, extrai o título
    e preço.
    Retorna um dicionário com os dados limpos.
    """
    # Headers para simular um navegador
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        #1. Extração do Título
        # Classe 'ui-pdp-title' é o padrão atual do ML para títulos de produtos
        title_tag = soup.find('h1', class_= 'ui-pdp-title')
        title = title_tag.text.strip() if title_tag else "Título não encontrado"

        # 2. Extração do Preço
        # O ML costuma guardar o valor principal nessa classe
        price_tag = soup.find('span', class_= 'andes-money-amount__fraction')
        price_cents_tag = soup.find('span', class_='andes-money-amount__cents')
        
        if price_tag:
            # Transformação (Data_cleaning):
            # O texto vem como "1.200" (com ponto para milhar). Precisamos tirar o ponto para virar float
            fraction = price_tag.text.replace(".", "")
            
            # Pega os centavos, se existirem.
            cents = price_cents_tag.text if price_cents_tag else "00"

            # Junta o inteiro e os centavos usando PONTO, e converte para float
            price_str = f"{fraction}.{cents}"
            price = float(price_str)

        else:
            price = 0.0

        # 3. Registro do momento exato da extração
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # retorna os dados organizados
        return {
            "url" : url,
            "Produto" : title,
            "preco" : price,
            "data_hora" : timestamp
        }
    except Exception as e:
        print(f"Erro ao processar a URL {url}: {e}")


def run_piperline(urls):
    """
    Função que orquestra o pipeline de ETL:
    garante a criação do banco, extrai os dados de cada URL e salva no SQLite.
    """
    # 1. Garante que o banco de dados e as tabelas estão prontos
    setup_database()

    print("\n Iniciando a rotina de extração e salvamento... ")

    # 2. Faz o loop (varre) pela lista de links
    for url in urls:
        print(f"\nExtraindo dados de: {url[:60]}...")

        # cahma o scraper (Extração + Transformação)
        dados = get_produto_data(url)

        if dados:
            # Chama o banco de dados (carga/load)
            save_data(dados)
        else:
            print(f" Falha na extração. Pulando para o próximo.")
    
    print("\n Processo diário finalizado com sucesso !")

# Bloco de execução principal
if __name__ == "__main__":
    # Lista de produtos que você quer monitorar
    urls_para_monitorar = [
        "https://www.mercadolivre.com.br/base-suporte-para-pc-notebook-aluminio-portatil-articulado-dobravel-tablet-laptop-mesa-davely-cor-prateado/p/MLB27065699#polycard_client=recommendations_home-deals&reco_backend=deals-model-odin&wid=MLB5579047914&reco_client=home-deals&reco_item_pos=4&reco_backend_type=low_level&reco_id=3a0d6f65-bfec-4f3c-972d-eef41b544ca0&sid=recos&c_id=/home/promotions-recommendations/element&c_uid=84337cf2-aae5-428b-b5d0-f960121b5f93",
        "https://www.mercadolivre.com.br/suporte-ajustavel-hytalux-notebook-macbook-11-a-17-aluminio-dobravel/p/MLB59142517#polycard_client=recommendations_pdp-v2p&reco_backend=ranker_retrieval_online_vpp_v2p&reco_model=coldstart_low_exposition&reco_client=pdp-v2p&reco_item_pos=0&reco_backend_type=low_level&reco_id=cbea90fd-8671-4688-b743-69b24b2f66cd&wid=MLB5067374120&sid=recos"
    ]

    # Executa a função principal passando a lista de URLs
    run_piperline(urls_para_monitorar)
