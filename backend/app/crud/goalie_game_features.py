from sqlalchemy import select, func, insert, not_, exists
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import GoalieGameFeatures, GoalieGameLog

async def update_goalie_game_features(db: AsyncSession):
    goalie_window_query = select(
        GoalieGameLog.game_id,
        GoalieGameLog.player_id,
        func.avg(GoalieGameLog.x_goals_against).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_x_goals_against"),
        func.avg(GoalieGameLog.goals_against).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_goals_against"),
        func.avg(GoalieGameLog.sog).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_sog"),
        func.avg(GoalieGameLog.flurry_adjusted_x_goals).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_flurry_adjusted_x_goals"),
        func.avg(GoalieGameLog.high_danger_x_goals).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_high_danger_x_goals"),
        func.avg(GoalieGameLog.x_sog).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_x_sog"),
        func.avg(GoalieGameLog.high_danger_shots).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_high_danger_shots"),
        func.avg(GoalieGameLog.rebounds).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_rebounds"),
        func.avg(GoalieGameLog.x_rebounds).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_x_rebounds"),
        func.avg(GoalieGameLog.freeze).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_freeze"),
        func.avg(GoalieGameLog.x_freeze).over(
            partition_by=GoalieGameLog.player_id, order_by=GoalieGameLog.game_date, rows=(-5, -1)
        ).label("rolling_x_freeze"),
    ).where(
        not_(
            exists().where(
                (GoalieGameFeatures.game_id == GoalieGameLog.game_id) &
                (GoalieGameFeatures.player_id == GoalieGameLog.player_id)
            )
        )
    )
    
    new_goalie_features = [row for row in (await db.execute(goalie_window_query)).mappings().all() if row["rolling_x_goals_against"] is not None]
    if new_goalie_features:
        await db.execute(insert(GoalieGameFeatures), new_goalie_features)
    await db.commit()