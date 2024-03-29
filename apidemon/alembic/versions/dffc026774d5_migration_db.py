"""migration db

Revision ID: dffc026774d5
Revises: 
Create Date: 2023-03-01 13:17:56.794513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dffc026774d5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('chat_id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('chat_id')
    )
    op.create_index(op.f('ix_user_user_id'), 'user', ['user_id'], unique=False)
    op.create_table('offer',
    sa.Column('offer_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('cost', sa.Integer(), nullable=True),
    sa.Column('desc', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('hidden', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('can_add_in_group', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('offer_id')
    )
    op.create_index(op.f('ix_offer_offer_id'), 'offer', ['offer_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_offer_offer_id'), table_name='offer')
    op.drop_table('offer')
    op.drop_index(op.f('ix_user_user_id'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
