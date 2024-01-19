import uuid
from pydantic import BaseModel


class SMenu(BaseModel):
    title: str
    description: str

class UUIDMenu(BaseModel):
    id: uuid.UUID