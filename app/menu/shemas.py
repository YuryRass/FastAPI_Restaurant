from pydantic import BaseModel


class SMenu(BaseModel):
    title: str
    description: str
