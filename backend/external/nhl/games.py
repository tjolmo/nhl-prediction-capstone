import httpx

async def fetch_and_get_players_in_a_game(game_id: int) -> list[int] | None:
    """Scrapes player data for a game from API, cleans, returns list of player IDs."""
    base_url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/boxscore"
    ids = []
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url)
            response.raise_for_status()
            data = response.json().get("playerByGameStats")
            if data and len(data) > 0:
                for team in ["homeTeam", "awayTeam"]:
                    forwards = data.get(team, {}).get("forwards", [])
                    defensemen = data.get(team, {}).get("defense", [])
                    goalies = data.get(team, {}).get("goalies", [])
                    all_players = forwards + defensemen + goalies
                    ids.extend([player.get("playerId") for player in all_players if player.get("playerId") is not None])
                return ids
            return None
        except Exception as e:
            print(f"Error scraping ID {game_id}: {e}")
            return None
