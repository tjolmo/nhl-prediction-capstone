from sqlalchemy import select, exists, not_, insert
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import TeamGameLog, TeamGameFeatures
from predictions.config import TEAM_BASE_STATS, TEAM_FEATURE_COLUMNS_SINGLE
import pandas as pd

async def update_team_game_features(db: AsyncSession):
    missing_query = select(
        TeamGameLog.game_id,
        TeamGameLog.team_tri_code,
        TeamGameLog.season,
    ).where(
        not_(
            exists().where(
                TeamGameFeatures.game_id == TeamGameLog.game_id,
                TeamGameFeatures.team_tri_code == TeamGameLog.team_tri_code
            )
        )
    )
    missing_rows = (await db.execute(missing_query)).all()
    if not missing_rows:
        return None

    missing_keys = {(r.game_id, r.team_tri_code) for r in missing_rows}
    team_seasons = {(r.team_tri_code, r.season) for r in missing_rows}

    all_features: list[dict] = []

    for team_tri_code, season in team_seasons:
        logs_query = (
            select(
                TeamGameLog.game_id, 
                TeamGameLog.team_tri_code, 
                TeamGameLog.game_date,
                *[getattr(TeamGameLog, s) for s in TEAM_BASE_STATS]
            )
            .where(
                TeamGameLog.team_tri_code == team_tri_code,
                TeamGameLog.season == season
            )
            .order_by(TeamGameLog.game_date)
        )
        logs = (await db.execute(logs_query)).mappings().all()
        if len(logs) < 6:  # need 5 prior + 1 current
            continue

        df = pd.DataFrame(logs)

        for stat in TEAM_BASE_STATS:
            df[f"rolling_{stat}_5g"] = (
                df[stat]
                .rolling(window=5, min_periods=5)
                .mean()
                .shift(1)
            )

        df["_key"] = list(zip(df["game_id"], df["team_tri_code"]))
        df = df[df["_key"].isin(missing_keys) & df["rolling_goals_5g"].notna()]

        if df.empty:
            continue

        records = df[["game_id", "team_tri_code"] + TEAM_FEATURE_COLUMNS_SINGLE].to_dict("records")

        # make sure no nan/na values
        for rec in records:
            for k, v in rec.items():
                if pd.isna(v):
                    rec[k] = None
        all_features.extend(records)

    if all_features:
        await db.execute(insert(TeamGameFeatures), all_features)
    await db.commit()

