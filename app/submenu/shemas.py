import uuid
from pydantic import BaseModel



class SSubMenu(BaseModel):
    title: str
    description: str

class SUUID(BaseModel):
    menu_id: str
    submenu_id: str