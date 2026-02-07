from pydantic import BaseModel, Field

class TeamResponse(BaseModel):
    id: int = Field(alias="id")
    name: str = Field(alias="fullName")
    franchise_id: int = Field(alias="franchiseId")
    tri_code: str = Field(alias="triCode")
    class Config:
        validate_by_name = True
