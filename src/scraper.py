import requests
from bs4 import BeautifulSoup
from datetime import datetime

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
            "preço" : price,
            "data_hora" : timestamp
        }
    except Exception as e:
        print(f"Erro ao processar a URL {url}: {e}")


if __name__ == "__main__":
    url_teste = "https://www.mercadolivre.com.br/base-suporte-para-pc-notebook-aluminio-portatil-articulado-dobravel-tablet-laptop-mesa-davely-cor-prateado/p/MLB27065699#polycard_client=recommendations_home-deals&reco_backend=deals-model-odin&wid=MLB5579047914&reco_client=home-deals&reco_item_pos=4&reco_backend_type=low_level&reco_id=3a0d6f65-bfec-4f3c-972d-eef41b544ca0&sid=recos&c_id=/home/promotions-recommendations/element&c_uid=84337cf2-aae5-428b-b5d0-f960121b5f93"
    print("Iniciando a extração...")

    dados = get_produto_data(url_teste)
    if dados:
        print("\n Extração conclúida com sucesso! ")
        print(f"Produto: {dados['Produto']}")
        print(f"Preço : R$ {dados['preço']}")
        print(f"Data/Hora : {dados['data_hora']}")
    else:
        print("\n Falha na extração. ")