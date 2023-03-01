"""migration db

Revision ID: 5952899d9c1b
Revises: 3c9f359eb364
Create Date: 2023-02-28 16:28:32.727626

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5952899d9c1b'
down_revision = '3c9f359eb364'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_request_log_request_log_id', table_name='request_log')
    op.drop_table('request_log')
    op.drop_index('ix_request_request_id', table_name='request')
    op.drop_index('ix_request_user_id', table_name='request')
    op.drop_table('request')
    op.drop_index('ix_groups_chat_id', table_name='groups')
    op.drop_index('ix_groups_group_id', table_name='groups')
    op.drop_table('groups')
    op.add_column('offer_photo', sa.Column('photo', sa.LargeBinary(), nullable=True))
    op.drop_constraint('offer_photo_photo_url_key', 'offer_photo', type_='unique')
    op.drop_column('offer_photo', 'photo_url')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('offer_photo', sa.Column('photo_url', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_unique_constraint('offer_photo_photo_url_key', 'offer_photo', ['photo_url'])
    op.drop_column('offer_photo', 'photo')
    op.create_table('groups',
    sa.Column('group_id', sa.INTEGER(), server_default=sa.text("nextval('groups_group_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('chat_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('busy', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.user_id'], name='groups_owner_id_fkey'),
    sa.PrimaryKeyConstraint('group_id', name='groups_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_groups_group_id', 'groups', ['group_id'], unique=False)
    op.create_index('ix_groups_chat_id', 'groups', ['chat_id'], unique=False)
    op.create_table('request',
    sa.Column('request_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('offer_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.group_id'], name='request_group_id_fkey'),
    sa.ForeignKeyConstraint(['offer_id'], ['offer.offer_id'], name='request_offer_id_fkey'),
    sa.PrimaryKeyConstraint('request_id', name='request_pkey')
    )
    op.create_index('ix_request_user_id', 'request', ['user_id'], unique=False)
    op.create_index('ix_request_request_id', 'request', ['request_id'], unique=False)
    op.create_table('request_log',
    sa.Column('request_log_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('info', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='request_log_user_id_fkey'),
    sa.PrimaryKeyConstraint('request_log_id', name='request_log_pkey')
    )
    op.create_index('ix_request_log_request_log_id', 'request_log', ['request_log_id'], unique=False)
    # ### end Alembic commands ###
