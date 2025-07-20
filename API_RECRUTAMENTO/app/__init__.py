from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from flasgger import Swagger


auth = HTTPBasicAuth()

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # incluir todas as rotas
            "model_filter": lambda tag: True,  # incluir todos os modelos
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "title": "Decision API Docs"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Decision - API de Previsão de Recrutamentos",
        "description": "API de previsão para ajudar com o recrutamento de candidatos utilizando modelos de Machine Learning.",
        "version": "1.0.0"
    }
}

app = Flask(__name__)
app.secret_key = "decision_chatbot_key"
swagger = Swagger(app,config=swagger_config, template=swagger_template)


@app.after_request
def remove_flasgger_logo(response):
    if response.content_type == "text/html; charset=utf-8" and "/apidocs" in str(request.url):
        response.direct_passthrough = False
        response.set_data(
            response.get_data(as_text=True).replace(
                "</head>",
                """
                <style>
                    .topbar-wrapper img { display: none !important; }
                    .topbar-wrapper span { visibility: hidden !important; }
                </style>
                </head>
                """
            )
        )
    return response

from app.utils import auth as auth_utils
from app.utils import auth_bigquery
from app.utils.auth_bigquery import df_applicants, df_prospects, df_vagas
from app.routes import auth_routes, previsao