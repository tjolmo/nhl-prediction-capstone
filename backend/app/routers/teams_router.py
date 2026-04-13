from app.crud.teams import search_teams_by_name
from fastapi import Query
from app.schemas.teams import TeamSearchResultOut
import datetime
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_db
from app.crud.teams import get_team_by_tri_code, check_tri_code_exists, get_team_current_roster, get_all_teams
from app.crud.games import get_all_games_for_date, get_next_n_games_info_by_tri_code, get_team_last_5_games
from app.schemas.teams import TeamBasicInfoOut, Last5GameInfoOut, TeamScheduledGameInfoOut, TeamRosteredPlayer

router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/last5/{tri_code}", status_code=200, response_model=list[Last5GameInfoOut])
async def get_last_5_games(tri_code: str, db = Depends(get_db)):
    if not await check_tri_code_exists(db, tri_code):
        raise HTTPException(status_code=404, detail=f"Team {tri_code} not found in DB")
    last_5 = await get_team_last_5_games(db, tri_code)
    if last_5 is not None:
        return [Last5GameInfoOut(game_id=game.id, date=game.date, home_team_tri_code=game.home_team_tri_code, away_team_tri_code=game.away_team_tri_code, home_score=game.home_score, away_score=game.away_score) for game in last_5]
    raise HTTPException(status_code=404, detail=f"No games found for Team {tri_code} in DB")

@router.get("/{tri_code}/basic_info", status_code=200, response_model=TeamBasicInfoOut)
async def get_team_basic_info(tri_code: str, db = Depends(get_db)):
    team = await get_team_by_tri_code(db, tri_code)
    if team is not None:
        return TeamBasicInfoOut(
            name=team.current_name,
            tricode=team.tri_code,
            logoUrl=f"https://assets.nhle.com/logos/nhl/svg/{team.tri_code}_light.svg" if team.tri_code else None
        )
    raise HTTPException(status_code=404, detail=f"Team {tri_code} not found in DB")

    
@router.get("/{tri_code}/next_5/{offset}", status_code=200, response_model=list[TeamScheduledGameInfoOut])
async def get_team_next_5_games(tri_code: str, offset: int, db = Depends(get_db)):
    next_5_games = await get_next_n_games_info_by_tri_code(db, tri_code, 5, offset)
    next_5_cleaned = []
    if next_5_games is not None:
        for i, game in enumerate(next_5_games):
            try: 
                home_team = await get_team_by_tri_code(db, game.home_team_tri_code)
                away_team = await get_team_by_tri_code(db, game.away_team_tri_code)
                homeTeam = TeamBasicInfoOut(name=home_team.current_name, 
                                            tricode=home_team.tri_code, 
                                            logoUrl=f"https://assets.nhle.com/logos/nhl/svg/{home_team.tri_code}_light.svg" if home_team.tri_code else None
                        )
                awayTeam = TeamBasicInfoOut(name=away_team.current_name, 
                                            tricode=away_team.tri_code, 
                                            logoUrl=f"https://assets.nhle.com/logos/nhl/svg/{away_team.tri_code}_light.svg" if away_team.tri_code else None
                        )
            except Exception as e:
                return HTTPException(status_code=500, detail=f"Error fetching team info for game {game.id}: {e}")
            next_5_cleaned.append(TeamScheduledGameInfoOut(
                id=game.id,
                date=datetime.datetime.strptime(str(game.date), "%Y%m%d").strftime("%B %d, %Y") if game.date else None,
                homeTeam=homeTeam,
                awayTeam=awayTeam,
                time=game.start_time,
                venue=game.venue,
                isNextGame=True if i == 0 else False
            ))
        return next_5_cleaned
    raise HTTPException(status_code=404, detail=f"No future games found for Team {tri_code} in DB")

@router.get("/games/{date}", status_code=200, response_model=list[TeamScheduledGameInfoOut])
async def get_all_games_from_date(db = Depends(get_db), date: str="today"):
    if date == "today":
        int_date = datetime.date.today()
        # to int YYYYMMDD
        int_date = int(int_date.strftime("%Y%m%d")) 
    else:
        try:
            int_date = int(date)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid date format. Please use YYYYMMDD or 'today'")

    games = await get_all_games_for_date(db, int_date)
    cleaned_games = []
    if games is None:
        raise HTTPException(status_code=404, detail=f"No games found for {date} in DB")
    for i, game in enumerate(games):
        try: 
            home_team = await get_team_by_tri_code(db, game.home_team_tri_code)
            away_team = await get_team_by_tri_code(db, game.away_team_tri_code)
            homeTeam = TeamBasicInfoOut(name=home_team.current_name, 
                                            tricode=home_team.tri_code, 
                                            logoUrl=f"https://assets.nhle.com/logos/nhl/svg/{home_team.tri_code}_light.svg" if home_team.tri_code else None
                        )
            awayTeam = TeamBasicInfoOut(name=away_team.current_name, 
                                            tricode=away_team.tri_code, 
                                            logoUrl=f"https://assets.nhle.com/logos/nhl/svg/{away_team.tri_code}_light.svg" if away_team.tri_code else None
                        )
        except Exception as e:
            return HTTPException(status_code=500, detail=f"Error fetching team info for game {game.id}: {e}")
        cleaned_games.append(TeamScheduledGameInfoOut(
            id=game.id,
            date=datetime.datetime.strptime(str(game.date), "%Y%m%d").strftime("%B %d, %Y") if game.date else None,
            homeTeam=homeTeam,
            awayTeam=awayTeam,
            time=game.start_time,
            venue=game.venue,
            isNextGame=False
        ))
    if len(cleaned_games) == 0:
        raise HTTPException(status_code=404, detail=f"No games found for today in DB")
    return cleaned_games

@router.get("/{tri_code}/current_roster", status_code=200, response_model=list[TeamRosteredPlayer] | None)
async def get_team_current_roster_endpoint(tri_code: str, db = Depends(get_db)):
    roster = await get_team_current_roster(db, tri_code)
    if roster is not None:
        return [TeamRosteredPlayer(
                    id=player.id, 
                    headshot=player.headshot,
                    first_name=player.first_name, 
                    current_team_tri_code=player.current_team_tri_code, 
                    position=player.position, 
                    last_name=player.last_name, 
                    number=player.number, 
                    shoots_catches=player.shoots_catches
                ) for player in roster]
    raise HTTPException(status_code=404, detail=f"Roster for Team {tri_code} not found in DB")

@router.get("/all", status_code=200, response_model=list[TeamBasicInfoOut])
async def get_all_teams_basic_info(db = Depends(get_db)):
    teams = await get_all_teams(db)
    if teams is not None:
        return_list = [TeamBasicInfoOut(name=team.current_name, tricode=team.tri_code, logoUrl=f"https://assets.nhle.com/logos/nhl/svg/{team.tri_code}_light.svg" if team.tri_code else None) for team in teams]
        # temp fix, no coyotes
        return_list.remove(TeamBasicInfoOut(name="Arizona Coyotes", tricode="ARI", logoUrl="https://assets.nhle.com/logos/nhl/svg/ARI_light.svg"))
        return return_list
    raise HTTPException(status_code=404, detail=f"No teams found in DB")

@router.get("/search", status_code=200, response_model=list[TeamSearchResultOut])
async def search_teams(q: str = Query(..., min_length=1), limit: int = 3, db=Depends(get_db)):
    """Searches teams by name."""
    results = await search_teams_by_name(db, q, limit)
    return [TeamSearchResultOut(
        name=team.current_name,
        tricode=team.tri_code,
        logoUrl=f"https://assets.nhle.com/logos/nhl/svg/{team.tri_code}_light.svg" if team.tri_code else None,
    ) for team in results]