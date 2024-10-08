"""update mobility results

Revision ID: 66140cf69a69
Revises: fa7c47d85bb9
Create Date: 2024-08-30 11:49:18.905606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66140cf69a69'
down_revision: Union[str, None] = 'fa7c47d85bb9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('mobility_result', 'main_objective_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('mobility_result_sub', 'sub_objective_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('mobility_result_sub', 'sub_objective_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('mobility_result', 'main_objective_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
