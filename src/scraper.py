import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
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
        return None

def buscar_links_de_pesquisa(search_term, limite_itens = 50):
    """
    Pesquisa um termo no Mercado Livre e retorna uma lista com as URLs dos produtos encontrados.
    """
    term_formatted = search_term.replace(" ", '-')
    url_pesquisa = f"https://lista.mercadolivre.com.br/{term_formatted}"

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url_pesquisa, headers=header)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # O ML usa a classe 'ui-search-link' para os links dos produtos na página de busca
        links_tags = soup.find_all('a', class_='poly-component__title')

        urls_encontradas = []
        for tag in links_tags:
            href = tag.get('href')
            # Evita adicionar links repetidos ou vazios
            if href and href not in urls_encontradas:
                urls_encontradas.append(href)
                # Para de procurar se já atingiu o limite desejado
                if len(urls_encontradas) >= limite_itens:
                    break

        return urls_encontradas        

    except Exception as e:
        print(f"Erro ao buscar o termo '{search_term}': {e}")
        return []
    
def search_and_save(search_term, max_produtos=10):
    """
    A função que orquestra tudo: Pega as URLs da busca e depois extrai cada página individualmente.
    """
    setup_database()

    print(f"\n Buscando links para: '{search_term}'...")
    urls = buscar_links_de_pesquisa(search_term, limite_itens= max_produtos)

    if not urls:
        print("Nenhum link encontrado. Cancelando extração.")
        return
    
    print(f" Encontrados {len(urls)} produtos. Iniciando extração detalhada (página por página) ... ")

    for i, url in enumerate(urls):
        print(f"\n[{i+1}/{len(urls)}] Lendo página do produto ...")
        dados = get_produto_data(url)

        if dados:
            save_data(dados)

        # Pausa amigável de 1 segundo para o Mercado Livre não bloquear nosso IP por excesso de requisições
        time.sleep(1)

    print("\n Processo de pesquisa e salvamento finalizado com sucesso!")

# Bloco de execução principal (Apenas para testarmos se tudo funciona)
if __name__ == "__main__":
    # Vamos testar pesquisando por monitores e limitando a apenas 3 produtos para ser rápido
    search_and_save("monitor gamer", max_produtos=3)