from pathlib import Path

SKATER_FEATURE_COLUMNS = [
    "rolling_x_goals",
    "rolling_toi",
    "rolling_game_score",
    "rolling_shot_attempts",
    "rolling_high_danger_shots",
    "rolling_on_ice_x_goals_percentage",
    "rolling_primary_assists",
    "rolling_goals",
    "rolling_points",
    "is_home",
]
SKATER_TARGET_COLUMNS = ["points", "goals", "primary_assists", "secondary_assists"]
SKATER_CLF_TARGET_COLUMNS = ["goals", "assists", "points"]
SKATER_MODEL_DIR = Path(__file__).parent / "models/skater"
SKATER_MODEL_DIR.mkdir(exist_ok=True)

def skater_model_path(target: str) -> Path:
    return SKATER_MODEL_DIR / f"{target}.joblib"
def skater_clf_model_path(target: str) -> Path:
    return SKATER_MODEL_DIR / f"{target}_clf.joblib"

SKATER_XGB_PARAMS = {
    "objective": "count:poisson",
    "tree_method": "hist",
    "eval_metric": "poisson-nloglik",
    "n_estimators": 1000,
    "learning_rate": 0.05,
    "max_depth": 3,
    "subsample": 0.8,
    "colsample_bytree": 1.0,
    "min_child_weight": 10,
    "random_state": 42,
    "verbosity": 0,
}
SKATER_XGB_CLF_PARAMS = {
    "objective": "binary:logistic",
    "n_estimators": 300,
    "max_depth": 5,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "min_child_weight": 3,
    "random_state": 42,
    "eval_metric": "logloss",
    "verbosity": 0,
}

GOALIE_FEATURE_COLUMNS = [
    "rolling_x_goals_against",
    "rolling_goals_against",
    "rolling_sog",
    "rolling_flurry_adjusted_x_goals",
    "rolling_high_danger_x_goals",
    "rolling_x_sog",
    "rolling_high_danger_shots",
    "rolling_rebounds",
    "rolling_x_rebounds",
    "rolling_freeze",
    "rolling_x_freeze",
    "is_home",
]
GOALIE_TARGET_COLUMNS = ["goals_against", "sog"]
GOALIE_CLF_TARGET_COLUMNS = ["shutout", "quality_start"]
GOALIE_MODEL_DIR = Path(__file__).parent / "models/goalie"
GOALIE_MODEL_DIR.mkdir(exist_ok=True)

def goalie_model_path(target: str) -> Path:
    return GOALIE_MODEL_DIR / f"goalie_{target}.joblib"
def goalie_clf_model_path(target: str) -> Path:
    return GOALIE_MODEL_DIR / f"goalie_{target}_clf.joblib"

GOALIE_XGB_PARAMS = {
    "objective": "count:poisson",
    "tree_method": "hist",
    "eval_metric": "poisson-nloglik",
    "n_estimators": 1000,
    "learning_rate": 0.05,
    "max_depth": 3,
    "subsample": 0.8,
    "colsample_bytree": 1.0,
    "min_child_weight": 10,
    "random_state": 42,
    "verbosity": 0,
}
GOALIE_XGB_CLF_PARAMS = {
    "objective": "binary:logistic",
    "n_estimators": 300,
    "max_depth": 5,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "min_child_weight": 3,
    "random_state": 42,
    "eval_metric": "logloss",
    "verbosity": 0,
}
