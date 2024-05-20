"""Remove temporary field

Revision ID: 2d609788c3bd
Revises: da311eb15855
Create Date: 2024-05-16 21:59:24.918348

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2d609788c3bd'
down_revision = 'da311eb15855'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('temp_field')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('temp_field', mysql.VARCHAR(length=10), nullable=True))

    # ### end Alembic commands ###
