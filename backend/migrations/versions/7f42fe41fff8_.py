"""empty message

Revision ID: 7f42fe41fff8
Revises: e7ae11cc6869
Create Date: 2023-11-20 10:12:24.461326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f42fe41fff8'
down_revision = 'e7ae11cc6869'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('original_price', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('current_price', sa.Float(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('current_price')
        batch_op.drop_column('original_price')

    # ### end Alembic commands ###