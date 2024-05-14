"""add foreign key to userinputs table

Revision ID: 1fde4c4d0ffd
Revises: 4b5e92962235
Create Date: 2024-05-14 23:01:41.603185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fde4c4d0ffd'
down_revision: Union[str, None] = '4b5e92962235'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('userinputs', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'userinput_user_fk', 
        source_table='userinputs', referent_table='users',
        local_cols=['user_id'], remote_cols=['id'],
        ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('userinput_user_fk', table_name='userinputs')
    op.drop_column('userinputs', 'user_id')
    pass
