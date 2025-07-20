import os
from google.cloud import bigquery
import pandas as pd

# Caminho relativo para o arquivo de credenciais
cred_path = os.path.join(os.path.dirname(__file__), '..', '..', 'credenciais.json')
cred_path = os.path.abspath(cred_path)  # transforma em caminho absoluto

# Define a variável de ambiente
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path

# Projeto GCP
project_id = "my-projects-462016"
client = bigquery.Client(project=project_id)

def consultar_tabela(nome_tabela, limite=None):
    query = f"SELECT * FROM `{project_id}.recrutamento_vagas.{nome_tabela}`"
    if limite is not None:
        query += f" LIMIT {limite}"
    df = client.query(query).result().to_dataframe()
    if limite is not None:
        print(f"\n Primeiros {limite} registros da tabela: {nome_tabela}")
        print(df.head())
    else:
        print(f"\n Todos os registros da tabela: {nome_tabela} foram carregados. Total: {len(df)} linhas.")
    return df

def consultar_prospects_com_dados(limite=None):
    query = f"""
    SELECT id, prospects, modalidade, titulo
    FROM `{project_id}.recrutamento_vagas.prospects`
    WHERE ARRAY_LENGTH(prospects) > 0
    """
    if limite is not None:
        query += f" LIMIT {limite}"
    df = client.query(query).result().to_dataframe()
    print(f"\nApós filtro, prospects com lista não vazia: {len(df)} linhas.")
    print(df.head())
    return df

# Carrega as tabelas
df_applicants = consultar_tabela("applicants", limite=None)
df_prospects = consultar_prospects_com_dados(limite=None)  # já com filtro no BigQuery
df_vagas = consultar_tabela("vagas", limite=None)