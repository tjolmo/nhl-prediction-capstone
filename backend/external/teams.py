import httpx
from .response_models import TeamResponse

BASE_URL = "https://api.nhle.com/stats/rest/en/team/id/{id}"

async def fetch_and_clean_team(team_id: int) -> TeamResponse | None:
    """Scrapes team data from API, cleans, returns"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BASE_URL.format(id=team_id))
            response.raise_for_status()
            data = response.json().get("data")
            if data and len(data) > 0:
                return TeamResponse(**data[0])
            return None
        except Exception as e:
            print(f"Error scraping ID {team_id}: {e}")
            return None

