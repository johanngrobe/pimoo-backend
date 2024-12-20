"""add is_published

Revision ID: 5ca630c1224c
Revises: 8e7ae8265451
Create Date: 2024-10-29 15:48:28.125122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ca630c1224c'
down_revision: Union[str, None] = '8e7ae8265451'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('climate_submission', sa.Column('is_published', sa.Boolean(), nullable=True))
    op.add_column('mobility_submission', sa.Column('is_published', sa.Boolean(), nullable=True))

    op.execute("UPDATE climate_submission SET is_published = false WHERE is_published IS NULL")
    op.execute("UPDATE mobility_submission SET is_published = false WHERE is_published IS NULL")

    op.alter_column('climate_submission', 'is_published', nullable=False)
    op.alter_column('mobility_submission', 'is_published', nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mobility_submission', 'is_published')
    op.drop_column('climate_submission', 'is_published')
    # ### end Alembic commands ###
