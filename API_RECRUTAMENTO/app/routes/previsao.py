from flask import Flask, request, jsonify
import pandas as pd
import joblib
import spacy
import logging
from app import app, auth, auth_bigquery, df_applicants, df_prospects, df_vagas

# === Configura log simples ===
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# === Carregar modelo ===
try:
    modelo = joblib.load('modelo/modelo_rf_final.pkl')
    logging.info("Modelo carregado com sucesso.")
except Exception as e:
    logging.error(f"Erro ao carregar modelo: {e}")
    raise

# === Carregar modelo spaCy ===
try:
    nlp = spacy.load('pt_core_news_sm')
    logging.info("Modelo spaCy carregado com sucesso.")
except OSError:
    logging.error("[ERRO] Modelo spacy 'pt_core_news_sm' não encontrado. Execute: python -m spacy download pt_core_news_sm")
    raise

# === Função para extrair entidades ===
def extrair_entidades(texto):
    doc = nlp(texto)
    return [(ent.text.lower(), ent.label_) for ent in doc.ents]

# === Dicionário com principais entidades ===
top_entidades = {
    'PER': ['ensino superior completo', 'pleno', 'ensino médio completo', 'srta', 'inicio', 'ensino', 'conhecimento', 'completo', 'budgeted rate', 'dra'],
    'ORG': ['p1', 'pj', 'p3 - advanced', 'sd', 'iso', 'pp', 'microsoft', 'ibm', 'itil', 'pmo'],
    'LOC': ['brasil', 'são paulo', 'avançado', 'intermediário', 'fechado', 'experiência', 'rio de janeiro', 'sp', 'minas gerais', 'fortaleza'],
    'MISC': ['básico', 'sap', 'ti - projetos-', 'r$', 'gestão', 'notebook', 'sql', 'alocação de recursos de ti-', 'oracle', 'java']
}

# === Endpoint /predict ===
@app.route('/predict', methods=['POST'])
@auth.login_required
def predict():
    
    """
    Prever Candidaturas com dados JSON
    ---
    tags:
      - Prever Candidaturas
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            formacao_e_idiomas:
              type: string
              example: "Ensino superior completo"
            cargo_atual:
              type: string
              example: "Analista"
            perfil_vaga:
              type: string
              example: "TI - Projetos"
            beneficios:
              type: string
              example: "Vale refeição"
            informacoes_profissionais:
              type: string
              example: "SQL e gestão"
            infos_basicas:
              type: string
              example: "São Paulo"
    responses:
      200:
        description: Previsão gerada com sucesso
      400:
        description: Requisição inválida
      500:
        description: Erro na previsão
    """
    try:
        dados = request.json

        colunas_entrada = ['formacao_e_idiomas', 'cargo_atual', 'perfil_vaga', 'beneficios',
                           'informacoes_profissionais', 'infos_basicas']

        for col in colunas_entrada:
            if col not in dados:
                dados[col] = ''

        df = pd.DataFrame([dados])
        df['texto_geral'] = df[colunas_entrada].astype(str).agg(' '.join, axis=1)
        df['entidades'] = df['texto_geral'].apply(extrair_entidades)

        for tipo, termos in top_entidades.items():
            for termo in termos:
                col = f"{tipo}_{termo}".replace(" ", "_").replace("-", "_").replace("$", "dollar").lower()
                df[col] = df['entidades'].apply(lambda lista: int(any(termo in ent_text for ent_text, ent_label in lista if ent_label == tipo)))

        for col in modelo.feature_names_in_:
            if col not in df.columns:
                df[col] = 0

        X = df[modelo.feature_names_in_]
        prob = modelo.predict_proba(X)[:, 1][0]
        pred = int(prob >= 0.75)

        return jsonify({'prob_contratacao': float(prob), 'contratado_predito': pred})

    except Exception as e:
        logging.error(f"Erro na previsão: {e}")
        return jsonify({'erro': str(e)}), 500