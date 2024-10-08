"""rename objetives

Revision ID: 1309540a7ffc
Revises: c9dc8f27f8ed
Create Date: 2024-08-28 17:52:04.505588

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1309540a7ffc'
down_revision: Union[str, None] = 'c9dc8f27f8ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.rename_table('key_target', 'main_objective')
    op.rename_table('sub_target', 'sub_objective')
    op.create_index(op.f('ix_main_objective_id'), 'main_objective', ['id'], unique=True)
    op.create_index(op.f('ix_sub_objective_id'), 'sub_objective', ['id'], unique=True)
    op.drop_index('ix_key_target_id', table_name='key_target')
    op.drop_index('ix_sub_target_id', table_name='sub_target')
    op.alter_column('mobility_result', 'key_target_id', new_column_name='main_objective_id')
    op.alter_column('mobility_result', 'key_target_bool', new_column_name='main_objective_bool')
    op.alter_column('mobility_result', 'sub_target_id', new_column_name='sub_objective_id')
    op.alter_column('mobility_result', 'sub_target_bool', new_column_name='sub_objective_bool')
    op.drop_constraint('mobility_result_sub_target_id_fkey', 'mobility_result', type_='foreignkey')
    op.drop_constraint('mobility_result_key_target_id_fkey', 'mobility_result', type_='foreignkey')
    op.create_foreign_key(None, 'mobility_result', 'sub_objective', ['sub_objective_id'], ['id'])
    op.create_foreign_key(None, 'mobility_result', 'main_objective', ['main_objective_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.rename_table('main_objective', 'key_target')
    op.rename_table('sub_objective', 'sub_target')
    op.alter_column('mobility_result', 'main_objective_id', new_column_name='key_target_id')
    op.alter_column('mobility_result', 'main_objective_bool', new_column_name='key_target_bool')
    op.alter_column('mobility_result', 'sub_objective_id', new_column_name='sub_target_id')
    op.alter_column('mobility_result', 'sub_objective_bool', new_column_name='sub_target_bool')
    op.drop_constraint('mobility_result_sub_target_id_fkey', 'mobility_result', type_='foreignkey')
    op.drop_constraint('mobility_result_key_target_id_fkey', 'mobility_result', type_='foreignkey')
    op.create_foreign_key(None, 'mobility_result', 'sub_objective', ['sub_objective_id'], ['id'])
    op.create_foreign_key(None, 'mobility_result', 'main_objective', ['main_objective_id'], ['id'])
    op.drop_constraint(None, 'mobility_result', type_='foreignkey')
    op.drop_constraint(None, 'mobility_result', type_='foreignkey')
    op.create_foreign_key('mobility_result_key_target_id_fkey', 'mobility_result', 'key_target', ['key_target_id'], ['id'])
    op.create_foreign_key('mobility_result_sub_target_id_fkey', 'mobility_result', 'sub_target', ['sub_target_id'], ['id'])
    op.create_index('ix_sub_target_id', 'sub_target', ['id'], unique=True)
    op.create_index('ix_key_target_id', 'key_target', ['id'], unique=True)
    op.drop_index(op.f('ix_sub_objective_id'), table_name='sub_objective')
    op.drop_index(op.f('ix_main_objective_id'), table_name='main_objective')
    # ### end Alembic commands ###
