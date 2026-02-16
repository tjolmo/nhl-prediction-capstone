from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_db
from external.nhl.teams import fetch_and_clean_team, fetch_and_clean_team_roster
from app.crud.teams import upsert_team, get_team_by_id, check_tri_code_exists
from app.crud.team_history import upsert_team_history
from app.schemas.teams import TeamInfoOut, TeamRosterAddOut
from app.crud.players import upsert_scraped_player

router = APIRouter(prefix="/teams", tags=["teams"])

@router.post("/add/current/{team_id}", status_code=200, response_model=TeamInfoOut)
async def add_current_team_data(team_id: int, db = Depends(get_db)):
    team_data, team_history_data = await fetch_and_clean_team(team_id)
    if team_data and team_history_data:
        await upsert_team(db, team_data)
        await upsert_team_history(db, team_history_data)
        return TeamInfoOut(id=team_history_data.id, name=team_data.current_name, franchise_id=team_data.franchise_id, tri_code=team_data.tri_code)
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

@router.post("/add/roster/{tri_code}/{season}", status_code=200, response_model=TeamRosterAddOut)
async def add_team_roster(tri_code: str, season: str, db = Depends(get_db)):
    
    if not await check_tri_code_exists(db, tri_code):
        raise HTTPException(status_code=404, detail=f"Team {tri_code} not found in DB")
    roster_data = await fetch_and_clean_team_roster(tri_code, season)
    if roster_data:
        num_players_added = 0
        for player in roster_data:
            if season=="current":
                await upsert_scraped_player(db, player, tri_code)
            else:
                await upsert_scraped_player(db, player)
            num_players_added += 1
        return TeamRosterAddOut(team=tri_code, season=season, roster_added=True, num_players_added=num_players_added)
    raise HTTPException(status_code=404, detail=f"Roster for Team {tri_code} Season {season} not found in external API")
