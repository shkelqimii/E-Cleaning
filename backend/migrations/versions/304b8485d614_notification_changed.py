"""notification changed

Revision ID: 304b8485d614
Revises: 3d7869d16e89
Create Date: 2023-11-08 11:12:05.169824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '304b8485d614'
down_revision = '3d7869d16e89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_user_created', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('description', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.drop_column('description')
        batch_op.drop_column('is_user_created')

    # ### end Alembic commands ###