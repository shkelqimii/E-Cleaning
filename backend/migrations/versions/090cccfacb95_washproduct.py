"""washproduct

Revision ID: 090cccfacb95
Revises: b06ec018e7c9
Create Date: 2023-12-07 15:13:19.499915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '090cccfacb95'
down_revision = 'b06ec018e7c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('washproducts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('washproducts')
    # ### end Alembic commands ###
