import httpx
from .response_models import TeamResponse, PlayerResponse

async def fetch_and_clean_team(team_id: int) -> TeamResponse | None:
    """Scrapes team data from API, cleans, returns"""
    base_url = f"https://api.nhle.com/stats/rest/en/team/id/{team_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url)
            response.raise_for_status()
            data = response.json().get("data")
            if data and len(data) > 0:
                return TeamResponse(**data[0])
            return None
        except Exception as e:
            print(f"Error scraping ID {team_id}: {e}")
            return None

async def fetch_and_clean_team_roster(team_tricode: str, season: str="current") -> list[PlayerResponse] | None:
    base_url = f"https://api-web.nhle.com/v1/roster/{team_tricode}/{season}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url, follow_redirects=True)
            response.raise_for_status()
            # get forwards, defensemen, goalies
            forwards = response.json().get("forwards", [])
            defensemen = response.json().get("defensemen", [])
            goalies = response.json().get("goalies", [])
            all_players = forwards + defensemen + goalies
            if all_players and len(all_players) > 0:
                return [PlayerResponse(**player) for player in all_players]
            return None
        except Exception as e:
            print(f"Error scraping Team {team_tricode} Season {season} Roster: {e}")
            return None

