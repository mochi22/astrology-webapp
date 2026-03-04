from pydantic import BaseModel

class PunishmentCreate(BaseModel):
    content: str
    category: str

class PunishmentUpdate(BaseModel):
    content: str
    category: str

class PunishmentResponse(BaseModel):
    id: int
    content: str
    category: str
    likes: int

    class Config:
        from_attributes = True