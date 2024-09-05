"""delete cascade

Revision ID: c5cfeb408455
Revises: d47b21bc9892
Create Date: 2024-09-05 18:53:35.819048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5cfeb408455'
down_revision: Union[str, None] = 'd47b21bc9892'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('mobility_result_submission_id_fkey', 'mobility_result', type_='foreignkey')
    op.create_foreign_key(None, 'mobility_result', 'mobility_submission', ['submission_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('mobility_result_sub_mobility_result_id_fkey', 'mobility_subresult', type_='foreignkey')
    op.create_foreign_key(None, 'mobility_subresult', 'mobility_result', ['mobility_result_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'mobility_subresult', type_='foreignkey')
    op.create_foreign_key('mobility_result_sub_mobility_result_id_fkey', 'mobility_subresult', 'mobility_result', ['mobility_result_id'], ['id'])
    op.drop_constraint(None, 'mobility_result', type_='foreignkey')
    op.create_foreign_key('mobility_result_submission_id_fkey', 'mobility_result', 'mobility_submission', ['submission_id'], ['id'])
    # ### end Alembic commands ###
