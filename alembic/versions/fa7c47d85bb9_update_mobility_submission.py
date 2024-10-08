"""update mobility submission

Revision ID: fa7c47d85bb9
Revises: 30fcc8a0697d
Create Date: 2024-08-30 11:43:17.686023

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa7c47d85bb9'
down_revision: Union[str, None] = '30fcc8a0697d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('mobility_submission', 'submission_no', new_column_name='administration_no', type_=sa.String(), nullable=False)
    op.alter_column('mobility_submission', 'submission_date', new_column_name='administration_date', type_=sa.Date(), nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('mobility_submission', 'administration_date', new_column_name='submission_date', type_=sa.DATE(), nullable=False)
    op.alter_column('mobility_submission', 'administration_no', new_column_name='submission_no', type_=sa.INTEGER(), nullable=False)
    # ### end Alembic commands ###
