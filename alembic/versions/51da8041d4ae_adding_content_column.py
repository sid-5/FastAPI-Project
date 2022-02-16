"""adding content column

Revision ID: 51da8041d4ae
Revises: 0ea3a0494645
Create Date: 2022-02-16 21:45:11.952795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51da8041d4ae'
down_revision = '0ea3a0494645'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
