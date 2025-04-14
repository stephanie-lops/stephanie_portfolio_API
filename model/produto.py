from sqlalchemy import Column, String, Integer, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

class Produto(Base):
    __tablename__ = 'produto'

    id = Column(Integer, primary_key=True)
    nome = Column(String(140), nullable=False)
    email = Column(String(140), nullable=False)
    quantity = Column(Integer, default=1)

    data_insercao = Column(DateTime, default=datetime.now)

    __table_args__ = (UniqueConstraint('nome', 'email', name='_nome_email_uc'),)

    def __init__(self, nome: str, email: str, quantity: int = 1,
             data_insercao: Union[DateTime, None] = None):
        """
        Creates a Client

        Arguments:
            nome: client's name
            email: client's email
            quantity: optional data (e.g., number of subscriptions)
            data_insercao: timestamp when the client was added
        """
        self.nome = nome
        self.email = email
        self.data_insercao = data_insercao or datetime.now()
