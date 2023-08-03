"""Initilize negative_karmalego_status

Revision ID: f9c8f0f2fd23
Revises: 
Create Date: 2023-06-20 22:54:04.951322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9c8f0f2fd23'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('visualization', schema=None) as batch_op:
        batch_op.add_column(sa.Column('NKL_id', sa.String(length=150), nullable=True))
        batch_op.create_foreign_key(None, 'negative_karma_lego', ['NKL_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('visualization', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('NKL_id')

    # ### end Alembic commands ###