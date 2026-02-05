# 📉 Rastreador de Preços e Oportunidades (End-to-End)

> 🚧 **Status do Projeto:** Em Desenvolvimento (Estrutura Base) 🚧

Este projeto é uma solução de Ciência de Dados End-to-End projetada para monitorar preços de produtos em e-commerce, armazenar o histórico e identificar os melhores momentos de compra.

## 🎯 Objetivo
Demonstrar a construção de um pipeline de dados completo, saindo do ambiente de notebook para uma aplicação funcional:
1.  **Coleta (ETL):** Web Scraping robusto com tratamento de erros.
2.  **Armazenamento:** Banco de dados SQL para histórico temporal.
3.  **Visualização:** Dashboard interativo para análise de tendências.
4.  **Automação:** Execução agendada via CI/CD.

## 📂 Estrutura do Projeto
A organização segue padrões de Engenharia de Software aplicados a Dados:

* `src/`: Código fonte da aplicação.
    * `scraper.py`: Scripts de extração (Coleta).
    * `database.py`: Gerenciamento do banco de dados (Armazenamento).
    * `app.py`: Dashboard interativo (Visualização).
* `data/`: Diretório para o banco de dados local (SQLite).
* `notebooks/`: Área para prototipagem e Análise Exploratória (EDA).
* `.github/workflows/`: Scripts de automação do GitHub Actions.

## 🛠️ Tecnologias
* **Linguagem:** Python
* **Coleta:** Request, BeautifulSoup
* **Dados:** SQLite, Pandas, SQLAlchemy
* **Frontend:** Streamlit