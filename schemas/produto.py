from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from model.produto import Produto
from model import Produto


from flask_openapi3 import APIView, Schema, request


class ProdutoSchema(BaseModel):
    """ Defines how a new product to be inserted should be represented """
    nome: str
    email: str

class ProdutoBuscaSchema(BaseModel):
    """ Defines the structure for the search. It will be based on the name and email. """
    nome: str
    email: str


class ProdutoBuscaFlexivelSchema(BaseModel):
    nome: Optional[str] = Field(None, description="Nome(opcional): ")
    email: Optional[str] = Field(None, description="Email(opcional):")


class ListagemProdutosSchema(BaseModel):
    """ Defines how a listing of products will be returned. """
    produtos: List[ProdutoSchema]


def apresenta_produtos(produtos: List[Produto]):
    """ Returns a representation of the products following the schema defined in ProdutoViewSchema. """
    result = []
    for produto in produtos:
        result.append({
            "nome": produto.nome,
            "email": produto.email,
           # "quantity": produto.quantity,
        })

    return {"produtos": result}


class ProdutoViewSchema(BaseModel):
    """ Defines how a product will be returned. """
    id: int = 1
    nome: str = "Client Example"
    email: str = "client@example.com"
    quantity: int = 5


class ProdutoDelSchema(BaseModel):
    """ Defines the structure of the data returned after a removal request. """
    message: str
    nome: str
    email: str


def apresenta_produto(produto: Produto):
    """ Returns a representation of the product following the schema defined in ProdutoViewSchema. """
    return {
        "id": produto.id,
        "nome": produto.nome,
        "email": produto.email,

    }

class ProdutoUpdateSchema(BaseModel):
    originalName: str = Field(..., example="Current Name")
    originalEmail: str = Field(..., example="Current E-mail")
    nome: str = Field(..., example="New Name")
    email: str = Field(..., example="New E-mail")



class ContactFormSchema(BaseModel):
    nome: str
    email: EmailStr
    mensagem: str

