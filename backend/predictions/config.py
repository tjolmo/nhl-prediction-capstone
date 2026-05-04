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
    "objective": "reg:tweedie",
    "tweedie_variance_power": 1.4,
    "tree_method": "hist",
    "eval_metric": "tweedie-nloglik@1.4",
    "n_estimators": 3000,
    "learning_rate": 0.015,
    "max_depth": 4,
    "subsample": 0.7,
    "colsample_bytree": 0.7,
    "colsample_bylevel": 0.7,
    "min_child_weight": 15,
    "reg_alpha": 0.5,
    "reg_lambda": 2.0,
    "random_state": 42,
    "verbosity": 0,
    "early_stopping_rounds": 75,
}

SKATER_XGB_CLF_PARAMS = {
    "objective": "binary:logistic",
    "tree_method": "hist",
    "eval_metric": "logloss",
    "n_estimators": 2000,
    "learning_rate": 0.02,
    "max_depth": 4,
    "subsample": 0.7,
    "colsample_bytree": 0.7,
    "colsample_bylevel": 0.7,
    "min_child_weight": 10,
    "reg_alpha": 0.3,
    "reg_lambda": 1.5,
    "random_state": 42,
    "verbosity": 0,
    "early_stopping_rounds": 75,
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
GOALIE_MODEL_DIR = Path(__file__).parent / "models/goalie"
GOALIE_MODEL_DIR.mkdir(exist_ok=True)

def goalie_model_path(target: str) -> Path:
    return GOALIE_MODEL_DIR / f"goalie_{target}.joblib"

GOALIE_XGB_PARAMS = {
    "objective": "reg:tweedie",
    "tweedie_variance_power": 1.4,
    "tree_method": "hist",
    "eval_metric": "tweedie-nloglik@1.4",
    "n_estimators": 3000,
    "learning_rate": 0.02,
    "max_depth": 4,
    "subsample": 0.7,
    "colsample_bytree": 0.7,
    "colsample_bylevel": 0.7,
    "min_child_weight": 10,
    "reg_alpha": 0.3,
    "reg_lambda": 2.0,
    "random_state": 42,
    "verbosity": 0,
    "early_stopping_rounds": 100,
}

TEAM_BASE_STATS = [
    "goals", "x_goals", "shot_attempts", "high_danger_shots",
    "points", "primary_assists", "avg_on_ice_x_goals_percentage",
    "avg_game_score", "goals_against", "x_goals_against",
    "sog_against", "high_danger_shots_against",
    "high_danger_x_goals_against", "flurry_adjusted_x_goals_against",
]
TEAM_WINDOW = 5
TEAM_FEATURE_COLUMNS_SINGLE = [f"rolling_{s}_5g" for s in TEAM_BASE_STATS]
TEAM_OPP_FEATURE_COLUMNS = [f"opp_{c}" for c in TEAM_FEATURE_COLUMNS_SINGLE]
TEAM_FEATURE_COLUMNS = TEAM_FEATURE_COLUMNS_SINGLE + ["is_home"] + TEAM_OPP_FEATURE_COLUMNS
TEAM_CLF_TARGET_COLUMNS = ["win"]

TEAM_MODEL_DIR = Path(__file__).parent / "models/team"
TEAM_MODEL_DIR.mkdir(exist_ok=True)

def team_clf_model_path(target: str) -> Path:
    return TEAM_MODEL_DIR / f"team_{target}_clf.joblib"

TEAM_XGB_CLF_PARAMS = {
    "objective": "binary:logistic",
    "tree_method": "hist",
    "eval_metric": "logloss",
    "n_estimators": 2000,
    "learning_rate": 0.04,
    "max_depth": 4,
    "subsample": 0.7,
    "colsample_bytree": 0.7,
    "colsample_bylevel": 0.7,
    "min_child_weight": 10,
    "reg_alpha": 0.3,
    "reg_lambda": 1.5,
    "random_state": 42,
    "verbosity": 0,
    "early_stopping_rounds": 75,
}