from pydantic import BaseModel
from datetime import datetime

class PlayerBase(BaseModel):
    name: str
    team: str
    position: str
    number: int

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(PlayerBase):
    pass

class PlayerResponse(PlayerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True