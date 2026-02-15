from pydantic import BaseModel

class TeamInfoOut(BaseModel):
    id: int
    name: str
    franchise_id: int
    tri_code: str

    class Config:
        from_attributes = True

class TeamRosterAddOut(BaseModel):
    team: str
    season: str
    roster_added: bool
    num_players_added: int

    class Config:
        from_attributes = True