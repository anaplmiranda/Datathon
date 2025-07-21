# 🧠 Projeto Datathon - Machine Learning Engineering

Baseado no estudo de caso da empresa fictícia **Decision**, que atua no setor de bodyshop e possui foco em alocar talentos ideais para os clientes de forma eficiente.

<div align="center">
  <p float="left" align="middle">
    <img src="https://www.fiap.com.br/wp-content/themes/fiap2016/images/sharing/fiap.png" alt="Logo FIAP" width="300"/>
  </p>
</div>

[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://python.org)
[![FastAPI Version](https://img.shields.io/badge/fastapi-0.110.0-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-final-orange)](/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![FIAP](https://img.shields.io/badge/FIAP-project-red.svg)](https://www.fiap.com.br)
[![API](https://img.shields.io/badge/API-REST-yellow.svg)](/)

---

## 📋 Sobre o Projeto

Este projeto foi desenvolvido em grupo como entrega final do curso **Pós Tech - Machine Learning Engineering (MLET)** da FIAP.  
Nosso objetivo foi usar Inteligência Artificial para otimizar o processo de recrutamento e seleção da empresa fictícia **Decision**, criando um modelo preditivo que auxilie no match entre candidatos e vagas.

---

## 🗂 Sumário

- [Visão Geral](#🎯-visão-geral)
- [Estrutura do Projeto](#📁-estrutura-do-projeto)
- [Documentação](#📄-documentação)
- [Tecnologias](#🛠-tecnologias)
- [Instalação](#⚙️-instalação)
- [Uso](#💻-uso)
- [Endpoints](#🌐-endpoints)
- [Contato](#💬-contato)

---

## 🎯 Visão Geral

Desenvolvemos um pipeline completo:
- Análise exploratória dos dados.
- Pré-processamento (incluindo balanceamento com SMOTE).
- Testes com modelos (Logistic Regression, Random Forest, XGBoost).
- Ajuste de hiperparâmetros.
- Modelo final salvo como **RF_final.pkl**.
- API FastAPI para receber dados JSON e retornar previsões.
- Empacotamento com Docker.
- Deploy disponível online.

---


## 📁 Estrutura do Projeto
notebooks/
  └── parte1_analise_exploratoria.ipynb
  └── parte2_modelagem_inferencia.ipynb

scripts/
  └── preprocessamento.py
  └── treinamento.py
  └── inferencia.py

model/
  └── RF_final.pkl

data/
  └── exemplo_input.json  (ou algum arquivo JSON que você tenha usado nos testes)
  └── predicoes.csv

api/
  └── app.py  (ou main.py, conforme usado para rodar a API)


---

## 📄 Documentação

- 🔗 GitHub Repo: [https://github.com/anaplmiranda/Datathon](https://github.com/anaplmiranda/Datathon)  
- 🌐 API online: [http://35.198.47.221:5000/](http://35.198.47.221:5000/)  
- API local (Swagger): `http://localhost:8000/docs`
---

## 🛠 Tecnologias

- Python 3.10
- FastAPI
- scikit-learn
- pandas / numpy
- imbalanced-learn (SMOTE)
- joblib / pickle
- Docker

---

## ⚙️ Instalação

1️⃣ Clone o repositório:
```bash
git clone https://github.com/anaplmiranda/Datathon.git
cd Datathon

3️⃣ Execute a API localmente:

bash
Copy
Edit
uvicorn api.app:app --reload
4️⃣ Ou execute via Docker:

bash
Copy
Edit
docker build -t datathon-api .
docker run -p 8000:8000 datathon-api


💻 Uso
Acesse no navegador (local):

bash
Copy
Edit
http://localhost:8000/docs
Ou use a versão em produção:

cpp
Copy
Edit
http://35.198.47.221:5000/


🌐 Endpoints
POST /predict: Recebe dados JSON e retorna previsão e probabilidade.

Exemplo de corpo JSON:

json
Copy
Edit
{
  "feature1": valor,
  "feature2": valor,
  "..."
}

💬 Contato
Grupo: [Adicionar nomes dos participantes]

🛡️ Observação
Este projeto foi desenvolvido exclusivamente para fins acadêmicos no contexto do Datathon MLET - FIAP.


