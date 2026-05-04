import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.team_game_logs import calculate_rolling_features_for_team
import joblib
from .config import (
    SKATER_TARGET_COLUMNS,
    SKATER_CLF_TARGET_COLUMNS,
    skater_model_path,
    skater_clf_model_path,
    GOALIE_TARGET_COLUMNS,
    goalie_model_path,
    TEAM_CLF_TARGET_COLUMNS,
    team_clf_model_path,
    TEAM_FEATURE_COLUMNS_SINGLE,
    TEAM_FEATURE_COLUMNS,
)

def load_skater_models() -> dict[str, object]:
    models: dict[str, object] = {}
    for target in SKATER_TARGET_COLUMNS:
        path = skater_model_path(target)
        if not path.exists():
            raise FileNotFoundError(
                f"No saved model for '{target}' at {path}.  "
            )
        models[target] = joblib.load(path)
    return models

def load_skater_clf_models() -> dict[str, object]:
    models: dict[str, object] = {}
    for target in SKATER_CLF_TARGET_COLUMNS:
        path = skater_clf_model_path(target)
        if not path.exists():
            raise FileNotFoundError(
                f"No saved classifier for '{target}' at {path}.  "
            )
        models[target] = joblib.load(path)
    return models

def load_goalie_models() -> dict[str, object]:
    models: dict[str, object] = {}
    for target in GOALIE_TARGET_COLUMNS:
        path = goalie_model_path(target)
        if not path.exists():
            raise FileNotFoundError(
                f"No saved model for '{target}' at {path}.  "
            )
        models[target] = joblib.load(path)
    return models

def load_team_clf_models() -> dict[str, object]:
    models: dict[str, object] = {}
    for target in TEAM_CLF_TARGET_COLUMNS:
        path = team_clf_model_path(target)
        if not path.exists():
            raise FileNotFoundError(
                f"No saved classifier for '{target}' at {path}.  "
            )
        models[target] = joblib.load(path)
    return models


async def get_upcoming_game_prediction(game, db: AsyncSession) -> list[float] | None:
    game_date_str = str(game.date)
    year = int(game_date_str[:4])
    month = int(game_date_str[4:6])
    # account for season start
    current_season = year if month >= 9 else year - 1

    # Calculate rolling features for both teams
    home_features_df = await calculate_rolling_features_for_team(db, game.home_team_tri_code, season=current_season)
    if home_features_df.empty:
        return None
    away_features_df = await calculate_rolling_features_for_team(db, game.away_team_tri_code, season=current_season)
    if away_features_df.empty:
        return None
    
    try:
        clf_models = load_team_clf_models()
    except FileNotFoundError as e:
        return None

    # transform into format for model
    home_row = home_features_df[TEAM_FEATURE_COLUMNS_SINGLE].copy()
    home_row["is_home"] = 1
    for col in TEAM_FEATURE_COLUMNS_SINGLE:
        home_row[f"opp_{col}"] = away_features_df[col].values[0]
    X_home = home_row[TEAM_FEATURE_COLUMNS].astype(np.float32)

    # make predictions
    prob_home_win = float(clf_models["win"].predict_proba(X_home)[:, 1][0])
    prob_away_win = 1.0 - prob_home_win
    return [prob_home_win, prob_away_win]