"""empty message

Revision ID: f1553e802731
Revises: 075e569fa217
Create Date: 2021-02-10 00:43:22.993159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1553e802731'
down_revision = '075e569fa217'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'ytsearch', ['video_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ytsearch', type_='unique')
    # ### end Alembic commands ###
