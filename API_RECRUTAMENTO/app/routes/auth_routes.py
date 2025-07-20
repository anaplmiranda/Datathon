from types import SimpleNamespace
from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from app import app, auth
import pdfplumber
import os
import re

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def extrair_texto_pdf(caminho_pdf):
    texto = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n"
    return texto

def extrair_info_cv(texto):
    info = {
        "nome": None,
        "endereco": None,
        "idade": None,
        "email": None,
        "telefone": None,
        "linkedin": None
    }

    linhas = texto.strip().split('\n')
    if linhas:
        info["nome"] = linhas[0].strip()

    email_match = re.search(r"[\w\.-]+@[\w\.-]+", texto)
    if email_match:
        info["email"] = email_match.group()

    telefone_match = re.search(r"(\(?\d{2}\)?\s?\d{4,5}-?\d{4})", texto)
    if telefone_match:
        info["telefone"] = telefone_match.group()

    linkedin_match = re.search(r"linkedin\.com/in/[\w\-]+", texto)
    if linkedin_match:
        info["linkedin"] = linkedin_match.group()

    endereco_match = re.search(r"(Rua|Av\.|Avenida|Travessa)\s+[^\n,]+[,\s]+\d+[^\n]*", texto)
    if endereco_match:
        info["endereco"] = endereco_match.group()

    idade_match = re.search(r"(\d{2})\s+anos", texto)
    if idade_match:
        info["idade"] = idade_match.group(1) + " anos"
    else:
        nascimento_match = re.search(r"(\d{2}/\d{2}/\d{4})", texto)
        if nascimento_match:
            info["idade"] = nascimento_match.group(1)

    return info

@app.route("/atualizar-dados", methods=["POST"])
def atualizar_dados():
    dados_atualizados = {
        "nome": request.form.get("nome"),
        "endereco": request.form.get("endereco"),
        "idade": request.form.get("idade"),
        "dt_nascimento": request.form.get("dt_nascimento"),
        "email": request.form.get("email"),
        "telefone": request.form.get("telefone"),
        "linkedin": request.form.get("linkedin"),
    }
    return render_template("final.html", dados=dados_atualizados)


def gerar_pergunta_personalizada(texto_cv):
    if "Python" in texto_cv:
        return "Vejo que você tem experiência com Python! Pode contar sobre seu projeto mais recente usando essa linguagem?"
    elif "Java" in texto_cv:
        return "Você menciona Java. Você trabalhou com backend ou Android?"
    else:
        return "Qual foi a tecnologia principal no seu último projeto?"

script_inicial = "Olá, obrigado(a) por participar desta conversa. A entrevista é composta por uma parte técnica e outra comportamental. Fique à vontade para responder com sinceridade — nosso foco é entender seu perfil e ver se há aderência com as oportunidades da Decision. Tudo bem?"
script_final = "Muito obrigado(a) por compartilhar sua trajetória conosco. Vamos analisar seu perfil junto ao time responsável pela vaga e te retornamos em breve."

perguntas_tecnicas = [
    "Qual sua última experiência com desenvolvimento de software?",
    "Quais linguagens de programação você domina?",
    "Você tem experiência com bancos de dados? Quais?",
    "Como você costuma versionar seus códigos?"
]

perguntas_comportamentais = [
    "Como você lida com prazos apertados?",
    "Conte sobre uma situação desafiadora que você enfrentou em equipe.",
    "Como você reage a feedbacks negativos?"
]

perguntas_engajamento = [
    "Por que você gostaria de trabalhar com a Decision?",
    "Você prefere trabalhar remoto, híbrido ou presencial?",
    "Quais são seus principais objetivos de carreira?"
]

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("cv")
        if not file:
            return render_template("index.html", erro="Nenhum arquivo enviado.")

        if not file.filename.lower().endswith(".pdf"):
            return render_template("index.html", erro="Formato inválido. Envie um arquivo PDF.")

        path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(path)

        texto = extrair_texto_pdf(path)
        dados_extraidos = extrair_info_cv(texto) 

        print("Dados extraídos:", dados_extraidos) 
        
        session["texto_cv"] = texto
        session["dados_extraidos"] = dados_extraidos

        return redirect(url_for("chat"))

    return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "texto_cv" not in session:
        return redirect(url_for("upload"))

    if "etapa" not in session:
        session["etapa"] = 0  # inicia direto na primeira pergunta
        session["respostas"] = []

        pergunta_extra = gerar_pergunta_personalizada(session["texto_cv"])
        session["perguntas"] = (
            perguntas_tecnicas
            + [pergunta_extra]
            + perguntas_comportamentais
            + perguntas_engajamento
            + [script_final]
        )

        return render_template("chat.html", pergunta=script_inicial, etapa=-1, is_final=False)

    etapa = session["etapa"]
    respostas = session["respostas"]
    perguntas = session["perguntas"]

    if request.method == "POST":
        if etapa < len(perguntas) - 1:
            resposta = request.form.get("resposta", "")
            respostas.append(resposta)

        session["etapa"] += 1
        etapa = session["etapa"]

        if etapa >= len(perguntas):
            perguntas_entrevista = session["perguntas"][1:-1]  # ignora script inicial e final
            respostas_usuario = session["respostas"]

            entrevista = list(zip(perguntas_entrevista, respostas_usuario))

            dados_cv_dict = session.get("dados_extraidos", {})
            dados_cv = SimpleNamespace(**dados_cv_dict)

            print("=== DEBUG FINAL ===")
            print("Texto do CV:", session.get("texto_cv", "")[:500])  # só os primeiros 500 caracteres
            print("Dados extraídos (dict):", session.get("dados_extraidos", {}))
            print("Respostas entrevista:", session.get("respostas", []))

            session.clear()
            return render_template("final.html", respostas=entrevista, dados=dados_cv)


    proxima_pergunta = perguntas[etapa] if etapa < len(perguntas) else None
    is_final = etapa == len(perguntas) - 1
    return render_template("chat.html", pergunta=proxima_pergunta, etapa=etapa, is_final=is_final)