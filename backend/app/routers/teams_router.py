from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_db
from external.teams import fetch_and_clean_team, fetch_and_clean_team_roster
from app.crud.teams import upsert_team, get_team_by_id, get_team_tricode_from_id
from app.schemas.teams import TeamInfoOut, TeamRosterAddOut
from app.crud.players import upsert_scraped_player

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

@router.post("/add/roster/{team_id}/{season}", status_code=200, response_model=TeamRosterAddOut)
async def add_team_roster(team_id: int, season: str, db = Depends(get_db)):
    team_tricode = await get_team_tricode_from_id(db, team_id)
    if not team_tricode:
        raise HTTPException(status_code=404, detail=f"Team {team_id} tricode not found in DB")
    roster_data = await fetch_and_clean_team_roster(team_tricode, season)
    if roster_data:
        num_players_added = 0
        for player in roster_data:
            if season=="current":
                await upsert_scraped_player(db, player, team_id)
            else:
                await upsert_scraped_player(db, player)
            num_players_added += 1
        return TeamRosterAddOut(team_id=team_id, season=season, roster_added=True, num_players_added=num_players_added)
    raise HTTPException(status_code=404, detail=f"Roster for Team {team_id} Season {season} not found in external API")
