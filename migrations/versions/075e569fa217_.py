"""empty message

Revision ID: 075e569fa217
Revises: 3f42febe4158
Create Date: 2021-02-09 18:46:00.150187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '075e569fa217'
down_revision = '3f42febe4158'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ytsearch', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ytsearch', sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
