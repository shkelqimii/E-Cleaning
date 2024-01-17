"""simplenotifications

Revision ID: b53b41364293
Revises: 304b8485d614
Create Date: 2023-11-08 13:22:51.511697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b53b41364293'
down_revision = '304b8485d614'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('simple_notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creator', sa.String(length=120), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('description', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('simple_notification', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_simple_notification_date'), ['date'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('simple_notification', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_simple_notification_date'))

    op.drop_table('simple_notification')
    # ### end Alembic commands ###
