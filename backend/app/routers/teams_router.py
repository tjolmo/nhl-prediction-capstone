from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_db
from external.teams import fetch_and_clean_team
from app.crud.teams import upsert_team, get_team_by_id
from app.schemas.teams import TeamInfoOut

router = APIRouter(prefix="/teams", tags=["teams"])

@router.post("/add/{team_id}", status_code=200, response_model=TeamInfoOut)
async def add_team_data(team_id: int, db = Depends(get_db)):
    team_data = await fetch_and_clean_team(team_id)
    if team_data:
        await upsert_team(db, team_data)
        return TeamInfoOut.model_validate(team_data)
    raise HTTPException(status_code=404, detail=f"Team {team_id} not found in external API")

@router.get("/get/{team_id}", response_model=TeamInfoOut, status_code=200)
async def get_stored_team_data(team_id: int, db = Depends(get_db)):
    try: 
        team_data = await get_team_by_id(db, team_id)
        if team_data:
            return team_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving team {team_id} from DB: {e}")
    raise HTTPException(status_code=404, detail=f"Team {team_id} not found in DB")