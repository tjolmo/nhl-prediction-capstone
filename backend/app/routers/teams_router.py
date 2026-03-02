import datetime

from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_db
from external.nhl.teams import fetch_and_clean_team_roster
from app.crud.teams import get_team_by_tri_code, check_tri_code_exists, update_team_roster_last_updated
from app.crud.games import get_date_most_recent_game_marked_as_future, get_next_n_games_info_by_tri_code, get_team_last_5_games, get_next_game_info_by_tri_code
from app.schemas.teams import NextGameInfoOut, TeamBasicInfoOut, TeamInfoOut, TeamRosterAddOut, Last5GameInfoOut, TeamScheduledGameInfoOut
from app.crud.players import upsert_scraped_player

router = APIRouter(prefix="/teams", tags=["teams"])

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
        await update_team_roster_last_updated(db, tri_code)
        return TeamRosterAddOut(team=tri_code, season=season, roster_added=True, num_players_added=num_players_added)
    raise HTTPException(status_code=404, detail=f"Roster for Team {tri_code} Season {season} not found in external API")

@router.get("/last5/{tri_code}", status_code=200, response_model=list[Last5GameInfoOut])
async def get_last_5_games(tri_code: str, db = Depends(get_db)):
    if not await check_tri_code_exists(db, tri_code):
        raise HTTPException(status_code=404, detail=f"Team {tri_code} not found in DB")
    last_5 = await get_team_last_5_games(db, tri_code)
    if last_5 is not None:
        return [Last5GameInfoOut(game_id=game.id, date=game.date, home_team_tri_code=game.home_team_tri_code, away_team_tri_code=game.away_team_tri_code, home_score=game.home_score, away_score=game.away_score) for game in last_5]
    raise HTTPException(status_code=404, detail=f"No games found for Team {tri_code} in DB")

@router.get("/nextgame/date/{tri_code}", status_code=200)
async def get_next_game_date(tri_code: str, db = Depends(get_db)):
    if not await check_tri_code_exists(db, tri_code):
        raise HTTPException(status_code=404, detail=f"Team {tri_code} not found in DB")
    next_game = await get_date_most_recent_game_marked_as_future(db, tri_code)
    if next_game is not None:
        return {"next_game_date": next_game}
    raise HTTPException(status_code=404, detail=f"No future games found for Team {tri_code} in DB")

@router.get("/nextgame/info/{tri_code}", status_code=200, response_model=NextGameInfoOut)
async def get_next_game_info(tri_code: str, db = Depends(get_db)):
    if not await check_tri_code_exists(db, tri_code):
        raise HTTPException(status_code=404, detail=f"Team {tri_code} not found in DB")
    next_game = await get_next_game_info_by_tri_code(db, tri_code)
    if next_game is not None:
        try:
            #date is int YYYYMMDD, convert to datetime without time
            next_game.date = datetime.datetime.strptime(str(next_game.date), "%Y%m%d").date()
        except Exception as e:
            print(f"Error converting game date for team {tri_code}: {e}")

        return NextGameInfoOut(
            game_id=next_game.id,
            date=next_game.date,
            home_team_tri_code=next_game.home_team_tri_code,
            away_team_tri_code=next_game.away_team_tri_code,
            venue=next_game.venue,
            start_time=next_game.start_time
        )
    raise HTTPException(status_code=404, detail=f"No future games found for Team {tri_code} in DB") 

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

    
@router.get("/{tri_code}/next_5", status_code=200, response_model=list[TeamScheduledGameInfoOut])
async def get_team_next_5_games(tri_code: str, db = Depends(get_db)):
    next_5_games = await get_next_n_games_info_by_tri_code(db, tri_code, 5)
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