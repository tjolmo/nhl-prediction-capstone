"""SkaterGameLog updates

Revision ID: b38821d5ec80
Revises: c192cda2248f
Create Date: 2026-02-16 07:44:25.937039

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b38821d5ec80'
down_revision: Union[str, Sequence[str], None] = 'c192cda2248f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('skater_game_logs', sa.Column('name', sa.String(), nullable=True))

    op.alter_column(
        'skater_game_logs',
        'game_date',
        existing_type=sa.VARCHAR(),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using="game_date::integer"
    )


def downgrade() -> None:
    op.alter_column(
        'skater_game_logs',
        'game_date',
        existing_type=sa.Integer(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
        postgresql_using="game_date::varchar"
    )

    op.drop_column('skater_game_logs', 'name')