
# tests/test_pipeline.py

from api.app import model
import pandas as pd


def test_model_prediction():
    # Dados de teste fake com as mesmas colunas do modelo
    data = pd.DataFrame([{
        "feature1": 1.5,
        "feature2": 0.8,
        "feature3": "valor"
    }])

    prediction = model.predict(data)
    assert prediction.shape[0] == 1  # Deve retornar 1 previsão
