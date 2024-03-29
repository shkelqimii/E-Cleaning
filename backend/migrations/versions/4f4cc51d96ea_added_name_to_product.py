"""Added name to Product

Revision ID: 4f4cc51d96ea
Revises: b44f2276bf1f
Create Date: 2023-10-06 10:49:26.421633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f4cc51d96ea'
down_revision = 'b44f2276bf1f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=255), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###
