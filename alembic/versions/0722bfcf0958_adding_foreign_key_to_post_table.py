"""adding foreign key to post table

Revision ID: 0722bfcf0958
Revises: 6805441e9177
Create Date: 2022-02-16 21:51:11.154815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0722bfcf0958'
down_revision = '6805441e9177'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
