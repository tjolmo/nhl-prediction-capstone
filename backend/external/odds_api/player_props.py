from external.odds_api.response_models import PlayerPropsResponse
from datetime import datetime
from external.odds_api.response_models import EventResponse
import os
import httpx

async def get_upcoming_games_odds_api(start_time: datetime, end_time: datetime) -> list[EventResponse]:
    """Gets event ids for upcoming games, used for props later"""
    async with httpx.AsyncClient() as client:
        base_url = "https://api.the-odds-api.com/v4/sports/icehockey_nhl/events"
        params = {
            "apiKey": os.getenv("ODDS_API_KEY"),
            "commenceTimeFrom": start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "commenceTimeTo": end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        response = await client.get(base_url, params=params)
        return [EventResponse(**event) for event in response.json()]

async def get_player_props(event_id: str) -> list[PlayerPropsResponse]:
    """Gets player props for a specific event_id"""
    async with httpx.AsyncClient() as client:
        base_url = f"https://api.the-odds-api.com/v4/sports/icehockey_nhl/events/{event_id}/odds"
        params = {
            "apiKey": os.getenv("ODDS_API_KEY"),
            "regions": "us",
            "markets": "player_points,player_assists,player_goals,player_total_saves",
            "oddsFormat": "american"
        }
        response = await client.get(base_url, params=params)
        results = response.json()
        return_list = []
        for bookmaker in results.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                prop_type = market.get("key")
                for outcome in market.get("outcomes", []):
                    name = outcome.get("description")
                    split_name = name.split(' ')
                    if len(split_name) >= 2:
                        first_name = split_name[0]
                        last_name = ' '.join(split_name[1:])
                    else:
                        continue
                    return_list.append(PlayerPropsResponse(
                        prop_type=prop_type,
                        first_name=first_name,
                        last_name=last_name,
                        line=outcome.get("point"),
                        odds=outcome.get("price"),
                        over_under=outcome.get("name")
                    ))
        return return_list
