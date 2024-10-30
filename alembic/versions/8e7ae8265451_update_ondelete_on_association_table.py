"""update ondelete on association table

Revision ID: 8e7ae8265451
Revises: e1ab718e686d
Create Date: 2024-10-28 16:40:00.349753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e7ae8265451'
down_revision: Union[str, None] = 'e1ab718e686d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('indicator_tag_tag_id_fkey', 'indicator_tag', type_='foreignkey')
    op.drop_constraint('indicator_tag_indicator_id_fkey', 'indicator_tag', type_='foreignkey')
    op.create_foreign_key(None, 'indicator_tag', 'tag', ['tag_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'indicator_tag', 'indicator', ['indicator_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'indicator_tag', type_='foreignkey')
    op.drop_constraint(None, 'indicator_tag', type_='foreignkey')
    op.create_foreign_key('indicator_tag_indicator_id_fkey', 'indicator_tag', 'indicator', ['indicator_id'], ['id'])
    op.create_foreign_key('indicator_tag_tag_id_fkey', 'indicator_tag', 'tag', ['tag_id'], ['id'])
    # ### end Alembic commands ###
