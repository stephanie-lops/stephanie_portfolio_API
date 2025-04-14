# PATCHES APLICADOS
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from schemas.produto import ProdutoBuscaFlexivelSchema
from schemas.produto import ContactFormSchema

from model import Session, Produto
from logger import logger
from schemas import *
from flask_cors import CORS 

import requests


def mascarar_email(email: str) -> str:
    nome, dominio = email.split("@")
    if len(nome) <= 3:
        parte_mascarada = "*" * len(nome)
    else:
        parte_mascarada = nome[:3] + "*" * (len(nome) - 3)
    return f"{parte_mascarada}@{dominio}"


info = Info(title="Stephanie's Portfolio Register Center", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app, origins=["http://localhost:3000"], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])


home_tag = Tag(name="Documentation", description="Select documentation: Swagger, Redoc or Rapnomeoc")
produto_tag = Tag(name="Client", description="Adding, viewing and removing clients from the database")

@app.get('/', tags=[home_tag])
def home():
    return redirect('/openapi')


# --------------------------------------------------------------------------------------
#   POST
# --------------------------------------------------------------------------------------

@app.post('/client', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(body: ProdutoSchema):
    nome = body.nome.strip().lower()
    email = body.email.strip().lower()

    logger.debug(f"Checking for existing Client: '{nome}', e-mail: '{email}'")
    try:
        session = Session()
        existing = session.query(Produto).filter(
            Produto.nome == nome,
            Produto.email == email
        ).first()

        if existing:
            error_msg = "Client with the same name and e-mail already exists in the database."
            logger.warning(f"Duplicate detected: {nome}, {email}")
            return {"message": error_msg}, 409

        produto = Produto(nome=nome, email=email, quantity=1)
        session.add(produto)
        session.commit()
        logger.debug(f"Client '{nome}' and e-mail '{email}' added")
        return apresenta_produto(produto), 200

    except IntegrityError:
        session.rollback()
        error_msg = "Client with the same name and e-mail already exists in the database."
        logger.warning(f"Integrity error on adding client '{nome}', '{email}'")
        return {"message": error_msg}, 409

    except Exception as e:
        session.rollback()
        error_msg = "Could not save the client."
        logger.warning(f"Unexpected error adding client '{nome}', {e}")
        return {"message": error_msg}, 400


# --------------------------------------------------------------------------------------
#   GET - ALL
# --------------------------------------------------------------------------------------

@app.get('/clients', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    logger.debug("Collecting products")
    session = Session()
    produtos = session.query(Produto).all()

    if not produtos:
        return {"produtos": []}, 200
    else:
        logger.debug(f"{len(produtos)} products found")
        return apresenta_produtos(produtos), 200


# --------------------------------------------------------------------------------------
#   GET - ONE ITEM
# --------------------------------------------------------------------------------------

@app.get('/client', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaFlexivelSchema):
    nome = query.nome
    email = query.email
    session = Session()

    if nome and email:
        logger.debug(f"Searching for client '{nome}' with e-mail '{email}'")
        produto = session.query(Produto).filter(Produto.nome == nome, Produto.email == email).first()

    elif nome:
        logger.debug(f"Searching for client with name '{nome}' (email forgotten)")
        produto = session.query(Produto).filter(Produto.nome == nome).first()

    else:
        return {"message": "Please provide at least a name or name and email."}, 400

    if not produto:
        logger.warning("Client not found in the database.")
        return {"message": "Client not found in the database."}, 404

    if not email:
        email_censurado = mascarar_email(produto.email)
        return {"email": email_censurado}, 200

    return apresenta_produto(produto), 200


# --------------------------------------------------------------------------------------
#   DELETE
# --------------------------------------------------------------------------------------

@app.delete('/client', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema, "400": ErrorSchema})
def del_produto(body: ProdutoBuscaSchema):
    nome = unquote(body.nome)
    email = body.email
    logger.debug(f"Deleting client '{nome}' with e-mail '{email}'")

    try:
        session = Session()
        count = session.query(Produto).filter(Produto.nome == nome, Produto.email == email).delete()
        session.commit()

        if count:
            logger.debug(f"Client '{nome}' with e-mail '{email}' deleted")
            return {"message": "Client removed", "nome": nome, "email": email}, 200
        else:
            error_msg = "Client not found in the database."
            logger.warning(f"Deletion failed: '{nome}' / '{email}': {error_msg}")
            return {"message": error_msg}, 404
    except Exception as e:
        error_msg = "Error deleting client. Please try again."
        logger.error(f"Deletion error for '{nome}' / '{email}': {e}")
        return {"message": error_msg}, 400


# --------------------------------------------------------------------------------------
#   PUT
# --------------------------------------------------------------------------------------

@app.put('/client', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_produto(body: ProdutoUpdateSchema):
    data = body.dict()
    try:
        session = Session()
        produto = session.query(Produto).filter(
            Produto.nome == data['originalName'],
            Produto.email == data['originalEmail']
        ).first()

        if not produto:
            error_msg = "Client not found in the database."
            logger.warning(f"Update failed for '{data['originalName']}': {error_msg}")
            return {"message": error_msg}, 404

        existing = session.query(Produto).filter(
            Produto.nome == data['nome'],
            Produto.email == data['email']
        ).first()

        if existing and existing.id != produto.id:
            error_msg = "A client with this name and e-mail already exists."
            logger.warning(f"Update conflict for '{data['nome']}', '{data['email']}'")
            return {"message": error_msg}, 400

        produto.nome = data['nome']
        produto.email = data['email']
        
        if 'quantity' in data and data['quantity'] is not None:
            produto.quantity = data['quantity']

        session.commit()
        logger.debug(f"Client updated: '{produto.nome}'")
        return apresenta_produto(produto), 200
    

    except IntegrityError:
        session.rollback()
        error_msg = "Integrity error while updating the client."
        logger.warning(f"Integrity error updating '{data['nome']}'")
        return {"message": error_msg}, 400

    except Exception as e:
        error_msg = "Error processing the request."
        logger.error(f"Unexpected error on update: {e}")
        return {"message": error_msg}, 400


# --------------------------------------------------------------------------------------
#   POST - CONTACT
# --------------------------------------------------------------------------------------


@app.post('/contact', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "400": ErrorSchema})
def contact_client(body: ContactFormSchema):
    nome = body.nome.strip()
    email = body.email.strip()
    mensagem = body.mensagem.strip()

    # 1. Salvar nome e email no banco
    try:
        session = Session()
        existing = session.query(Produto).filter(Produto.nome == nome, Produto.email == email).first()

        if not existing:
            novo = Produto(nome=nome, email=email, quantity=1)
            session.add(novo)
            session.commit()
            logger.debug(f"Novo cliente adicionado: {nome} ({email})")
        else:
            logger.debug(f"Cliente já existente: {nome} ({email})")

    except Exception as e:
        logger.error(f"Erro ao salvar no banco: {e}")
        return {"message": "Erro ao salvar no banco de dados."}, 400

    # 2. Enviar e-mail via Brevo
    try:
        brevo_api_key = "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"  # Chave API Brevo
        brevo_url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "api-key": brevo_api_key,
            "content-type": "application/json"
        }

        payload = {
            "sender": {"name": "Stephanie Portfolio", "email": "contactstephanielps@gmail.com"},  # FIXO
            "to": [{"email": "stephanielopees@gmail.com", "name": "Stephanie Lopes"}],  # RECEIVER
            "subject": "Novo contato do portfólio",
            "htmlContent": f"""
                <p><strong>Nome:</strong> {nome}</p>
                <p><strong>Email informado:</strong> {email}</p>
                <p><strong>Mensagem:</strong><br>{mensagem}</p>
            """
        }

        response = requests.post(brevo_url, json=payload, headers=headers)

        if response.status_code == 201:
            logger.info("Email enviado com sucesso via Brevo")
            return {"message": "Contato enviado com sucesso!"}, 200
        else:
            logger.error(f"Erro na API Brevo: {response.status_code} - {response.text}")
            return {"message": "Erro ao enviar o e-mail."}, 400

    except Exception as e:
        logger.error(f"Erro geral ao enviar contato: {e}")
        return {"message": "Erro ao processar o contato."}, 400
