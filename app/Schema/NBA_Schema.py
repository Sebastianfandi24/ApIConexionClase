from pydantic import BaseModel
from datetime import datetime

class PlayerBase(BaseModel):
    name: str
    team: str
    position: str
    

class PlayerCreate(PlayerBase):
    height_m: float
    weight_kg: float
    birth_date: datetime

class PlayerUpdate(PlayerBase):
    height_m: float
    weight_kg: float
    birth_date: datetime

class PlayerResponse(PlayerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True