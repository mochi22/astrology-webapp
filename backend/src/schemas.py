from pydantic import BaseModel

class PunishmentCreate(BaseModel):
    content: str
    category: str

class PunishmentResponse(BaseModel):
    id: int
    content: str
    category: str

    class Config:
        from_attributes = True