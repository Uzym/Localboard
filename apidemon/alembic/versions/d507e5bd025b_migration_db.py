"""migration db

Revision ID: d507e5bd025b
Revises: dffc026774d5
Create Date: 2023-03-02 14:50:52.848054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd507e5bd025b'
down_revision = 'dffc026774d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('offer', sa.Column('phoro', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('offer', 'phoro')
    # ### end Alembic commands ###