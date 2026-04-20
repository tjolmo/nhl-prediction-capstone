import joblib
from .config import (
    SKATER_TARGET_COLUMNS,
    SKATER_CLF_TARGET_COLUMNS,
    skater_model_path,
    skater_clf_model_path,
    GOALIE_TARGET_COLUMNS,
    GOALIE_CLF_TARGET_COLUMNS,
    goalie_model_path,
    goalie_clf_model_path,
)

def load_skater_models() -> dict[str, object]:
    models: dict[str, object] = {}
    for target in SKATER_TARGET_COLUMNS:
        path = skater_model_path(target)
        if not path.exists():
            raise FileNotFoundError(
                f"No saved model for '{target}' at {path}.  "
                f"Run training first:  python -m predictions.run skater"
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
                f"Run training first:  python -m predictions.run skater"
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
                f"Run training first:  python -m predictions.run goalie"
            )
        models[target] = joblib.load(path)
    return models

def load_goalie_clf_models() -> dict[str, object]:
    models: dict[str, object] = {}
    for target in GOALIE_CLF_TARGET_COLUMNS:
        path = goalie_clf_model_path(target)
        if not path.exists():
            raise FileNotFoundError(
                f"No saved classifier for '{target}' at {path}.  "
                f"Run training first:  python -m predictions.run goalie"
            )
        models[target] = joblib.load(path)
    return models