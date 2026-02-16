import pandas as pd
from .response_models import SkaterGameLogResponse

def scrape_skater_game_data(player_id: int) -> list[SkaterGameLogResponse] | None:
    csv_url = f"https://moneypuck.com/moneypuck/playerData/careers/gameByGame/regular/skaters/{player_id}.csv"
    cols= [
        'playerId', 'season', 'name', 'gameId', 'playerTeam', 
        'opposingTeam', 'gameDate', 'situation',
        'I_F_goals', 'I_F_primaryAssists', 'I_F_secondaryAssists', 'I_F_points',
        'I_F_xGoals', 'icetime', 'I_F_highDangerShots', 
        'I_F_shotAttempts', 'onIce_xGoalsPercentage', 'gameScore'
    ]

    # stop 403 error
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        df = pd.read_csv(
            csv_url, 
            usecols=cols, 
            storage_options=headers
        )
        # filters to last 3 seasons. All situations, meaning all game
        filtered = df.query('season >= 2023 and situation == "all"').copy()
        # convert to list of SkaterGameLogResponse
        return [SkaterGameLogResponse.model_validate(row) for row in filtered.to_dict("records")]
    except Exception as e:
        print(f"Error loading data: {e}")
        return None