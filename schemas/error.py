from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """ Defines how an error message will be represented
    """
    mesage: str
