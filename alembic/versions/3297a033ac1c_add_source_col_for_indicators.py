"""add source col for indicators

Revision ID: 3297a033ac1c
Revises: f765b1eeb897
Create Date: 2024-10-24 17:53:00.460545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3297a033ac1c'
down_revision: Union[str, None] = 'f765b1eeb897'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('indicator', sa.Column('source', sa.String(), nullable=True))
    op.add_column('indicator', sa.Column('source_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('indicator', 'source_url')
    op.drop_column('indicator', 'source')
    # ### end Alembic commands ###
