from pydantic import BaseModel, Field, field_validator

class TeamResponse(BaseModel):
    current_name: str = Field(alias="fullName")
    franchise_id: int = Field(alias="franchiseId")
    tri_code: str = Field(alias="triCode")
    class Config:
        validate_by_name = True

class TeamHistoryResponse(BaseModel):
    id: int = Field(alias="id")
    name: str = Field(alias="fullName")
    tri_code: str = Field(alias="triCode")

class PlayerResponse(BaseModel):
    id: int = Field(alias="id")
    headshot: str | None = Field(alias="headshot")
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    number: int | None = Field(default=None, alias="sweaterNumber")
    position: str | None = Field(alias="positionCode")
    shoots_catches: str | None = Field(alias="shootsCatches")
    
    # to get the english names 
    @field_validator("first_name", "last_name", mode="before")
    def extract_names(cls, v) -> str:
        if isinstance(v, dict) and "default" in v:
            return v["default"]
        return v

    class Config:
        validate_by_name = True
