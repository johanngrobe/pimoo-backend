"""user email unique

Revision ID: c099004fe40d
Revises: e14bf3114af2
Create Date: 2024-10-23 14:43:08.942208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c099004fe40d'
down_revision: Union[str, None] = 'e14bf3114af2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'user', ['id'])
    op.create_unique_constraint(None, 'user', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'user', type_='unique')
    # ### end Alembic commands ###