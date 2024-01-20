import uuid
from pydantic import BaseModel



class SSubMenu(BaseModel):
    title: str
    description: str
