"""add slots_per_day column to userinpts table

Revision ID: 8481ee4a1f95
Revises: a8627428af58
Create Date: 2024-05-14 22:04:00.477325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8481ee4a1f95'
down_revision: Union[str, None] = 'a8627428af58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'userinputs', 
        sa.Column('slots_per_day', sa.Integer, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('userinputs', 'slots_per_day')
    pass
