from pydantic import BaseModel

class TeamInfoOut(BaseModel):
    id: int
    name: str
    franchise_id: int
    tri_code: str

    class Config:
        from_attributes = True