# 🛒 Mercado Livre Price Tracker & Dashboard

## 📖 Sobre o Projeto
Este é um projeto de Ciência de Dados End-to-End (ponta a ponta) focado em monitoramento de preços. O objetivo principal é extrair dados de produtos do Mercado Livre, criar um histórico de preços em um banco de dados relacional e disponibilizar essas informações através de um painel interativo. 

O projeto simula um fluxo completo de **ETL** (Extração, Transformação e Carga), automatizando o acompanhamento de variações de valor no e-commerce.

## ⚙️ Arquitetura e Fluxo de Funcionamento
O sistema é dividido em três módulos principais, garantindo que o código seja limpo, modularizado e de fácil manutenção:

1. **`src/scraper.py` (Coleta e Transformação):**
   - Responsável por receber URLs de produtos.
   - Utiliza `requests` para baixar o HTML da página de forma veloz.
   - Utiliza `BeautifulSoup` para varrer o código, isolar e extrair o nome do produto e seu preço atual.
   - Realiza a limpeza dos dados (ex: conversão de texto para numérico) antes do envio.

2. **`src/database.py` (Armazenamento Inteligente):**
   - Cria e gerencia um banco de dados local utilizando **SQLite** (`data/prices.db`).
   - Modelado de forma relacional com duas tabelas: `produtos` (informações fixas) e `historico_precos` (valores e datas).
   - Contém a lógica de verificação: cadastra novos itens automaticamente ou apenas adiciona o preço do dia com *timestamp* para produtos já conhecidos, evitando duplicidade e criando uma linha do tempo confiável.

3. **`src/app.py` (Visualização / Dashboard):**
   - Lê as informações consolidadas no banco de dados.
   - Utiliza a biblioteca **Streamlit** para gerar uma interface web interativa.
   - Apresenta gráficos de linha com a evolução e queda dos preços e destaca indicadores chave, como o menor preço histórico registrado.

## 🛠️ Tecnologias e Requisitos
Para executar este projeto, você precisará do Python 3.9+ instalado e das seguintes bibliotecas:

- `requests` (Requisições HTTP)
- `beautifulsoup4` (Web Scraping / Parsing de HTML)
- `pandas` (Manipulação de dados)
- `sqlite3` (Banco de Dados nativo do Python)
- `streamlit` (Criação do Dashboard Web)

*(Veja o arquivo `requirements.txt` para as versões exatas).*

## 🚀 Como Executar Localmente

**1. Clone o repositório:**
```bash
git clone [https://github.com/CRalves-ops/Rastreador-de-precos](https://github.com/CRalves-ops/Rastreador-de-precos)
cd mercado_livre_tracker
