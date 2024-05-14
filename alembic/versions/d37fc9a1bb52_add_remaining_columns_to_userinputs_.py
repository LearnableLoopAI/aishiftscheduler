"""add remaining columns to userinputs table

Revision ID: d37fc9a1bb52
Revises: 1fde4c4d0ffd
Create Date: 2024-05-14 23:20:48.389281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd37fc9a1bb52'
down_revision: Union[str, None] = '1fde4c4d0ffd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# /////////////////////////////////////////////////////////////
    # max_daily_slot_run = Column(Integer, nullable=False)
    # resources = Column(String, nullable=False)
    # demands_per_busyness = Column(String, nullable=False)
    # demands_per_volume = Column(String, nullable=False)
    # demands_per_revenue = Column(String, nullable=False)
    # resource_expenses = Column(String, nullable=False)
    # created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # op.create_table(
    #     'users',
    #     sa.Column('id', sa.Integer(), nullable=False),
    #     sa.Column('email', sa.String(), nullable=False),
    #     sa.Column('password', sa.String(), nullable=False),
    #     sa.Column(
    #         'created_at',
    #         sa.TIMESTAMP(timezone=True),
    #         server_default=sa.text('now()'),
    #         nullable=False),
    #     sa.PrimaryKeyConstraint('id'),
    #     sa.UniqueConstraint('email')
    #     )

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def upgrade() -> None:
    op.add_column(
        'userinputs', 
        sa.Column('max_daily_slot_run', sa.Integer, nullable=False))
    op.add_column(
        'userinputs', 
        sa.Column('resources', sa.String, nullable=False))
    op.add_column(
        'userinputs', 
        sa.Column('demands_per_busyness', sa.String, nullable=False))
    op.add_column(
        'userinputs', 
        sa.Column('demands_per_volume', sa.String, nullable=False))
    op.add_column(
        'userinputs', 
        sa.Column('demands_per_revenue', sa.String, nullable=False))
    op.add_column(
        'userinputs', 
        sa.Column('resource_expenses', sa.String, nullable=False))
    op.add_column(
        'userinputs', 
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False)),
    pass

def downgrade() -> None:
    op.drop_column('userinputs', 'max_daily_slot_run')
    op.drop_column('userinputs', 'resources')
    op.drop_column('userinputs', 'demands_per_busyness')
    op.drop_column('userinputs', 'demands_per_volume')
    op.drop_column('userinputs', 'demands_per_revenue')
    op.drop_column('userinputs', 'resource_expenses')
    op.drop_column('userinputs', 'created_at')
    pass
