"""create userinputs table

Revision ID: a8627428af58
Revises: 
Create Date: 2024-05-11 20:00:37.374928

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8627428af58'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'userinputs', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('start', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('userinputs')
    pass
