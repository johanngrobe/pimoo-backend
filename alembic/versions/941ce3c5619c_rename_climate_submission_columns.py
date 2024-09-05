"""rename climate submission columns

Revision ID: 941ce3c5619c
Revises: 2f9170c7585a
Create Date: 2024-09-03 12:39:20.916130

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '941ce3c5619c'
down_revision: Union[str, None] = '2f9170c7585a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('climate_submission', 'submission_date', new_column_name='administration_date')
    op.alter_column('climate_submission', 'submission_no', new_column_name='administration_no')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('climate_submission', 'administration_no', new_column_name='submission_no')
    op.alter_column('climate_submission', 'administration_date', new_column_name='submission_date')
    # ### end Alembic commands ###
