from sqlalchemy import select, func, exists, insert, not_
from ..models import SkaterGameFeatures, SkaterGameLog
from sqlalchemy.ext.asyncio import AsyncSession

async def update_skater_game_features(db: AsyncSession) -> None:
    skater_window_query = select(
        SkaterGameLog.game_id,
        SkaterGameLog.player_id,
        func.avg(SkaterGameLog.x_goals).over(
            partition_by=SkaterGameLog.player_id, order_by=SkaterGameLog.game_date, rows=(-5, -1)
        ).label("rolling_x_goals"),
        func.avg(SkaterGameLog.toi).over(
            partition_by=SkaterGameLog.player_id, order_by=SkaterGameLog.game_date, rows=(-5, -1)
        ).label("rolling_toi"),
        func.avg(SkaterGameLog.game_score).over(
            partition_by=SkaterGameLog.player_id, order_by=SkaterGameLog.game_date, rows=(-5, -1)
        ).label("rolling_game_score"),
        func.avg(SkaterGameLog.shot_attempts).over(
            partition_by=SkaterGameLog.player_id, order_by=SkaterGameLog.game_date, rows=(-5, -1)
        ).label("rolling_shot_attempts"),
        func.avg(SkaterGameLog.high_danger_shots).over(
            partition_by=SkaterGameLog.player_id, order_by=SkaterGameLog.game_date, rows=(-5, -1)
        ).label("rolling_high_danger_shots"),
        func.avg(SkaterGameLog.on_ice_x_goals_percentage).over(
            partition_by=SkaterGameLog.player_id, order_by=SkaterGameLog.game_date, rows=(-5, -1)
        ).label("rolling_on_ice_x_goals_percentage"),
        func.avg(SkaterGameLog.primary_assists).over(
            partition_by=SkaterGameLog.player_id, order_by=SkaterGameLog.game_date, rows=(-5, -1)
        ).label("rolling_primary_assists"),
        func.avg(SkaterGameLog.goals).over(
            partition_by=SkaterGameLog.player_id, order_by=SkaterGameLog.game_date, rows=(-5, -1)
        ).label("rolling_goals"),
        func.avg(SkaterGameLog.points).over(
            partition_by=SkaterGameLog.player_id, order_by=SkaterGameLog.game_date, rows=(-5, -1)
        ).label("rolling_points")
    ).where(
        not_(
            exists().where(
                (SkaterGameFeatures.game_id == SkaterGameLog.game_id) &
                (SkaterGameFeatures.player_id == SkaterGameLog.player_id)
            )
        )
    )
    # Filter out None values
    new_skater_features = [row for row in (await db.execute(skater_window_query)).mappings().all() if row["rolling_x_goals"] is not None]
    if new_skater_features:
        await db.execute(insert(SkaterGameFeatures), new_skater_features)
    await db.commit()
