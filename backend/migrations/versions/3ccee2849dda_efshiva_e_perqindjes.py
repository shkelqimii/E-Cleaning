"""efshiva e perqindjes

Revision ID: 3ccee2849dda
Revises: ea691b4a3276
Create Date: 2023-12-15 14:14:24.882828

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3ccee2849dda'
down_revision = 'ea691b4a3276'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('discount_percentage')
        batch_op.drop_column('discounted_price')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('discounted_price', mysql.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('discount_percentage', mysql.FLOAT(), nullable=True))

    # ### end Alembic commands ###