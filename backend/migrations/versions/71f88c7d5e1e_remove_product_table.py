"""Remove Product table

Revision ID: 71f88c7d5e1e
Revises: 4f4cc51d96ea
Create Date: 2023-10-06 11:18:17.477997

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '71f88c7d5e1e'
down_revision = '4f4cc51d96ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('photo', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('price', mysql.FLOAT(), nullable=False),
    sa.Column('description', mysql.TEXT(), nullable=True),
    sa.Column('quantity', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
