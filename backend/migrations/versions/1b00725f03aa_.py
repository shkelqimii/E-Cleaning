"""empty message

Revision ID: 1b00725f03aa
Revises: 060e6f8e8bfa
Create Date: 2023-11-02 15:14:18.798376

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1b00725f03aa'
down_revision = '060e6f8e8bfa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=20), nullable=False))
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
        batch_op.drop_column('status')

    # ### end Alembic commands ###