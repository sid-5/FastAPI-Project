"""adding user table

Revision ID: 6805441e9177
Revises: 51da8041d4ae
Create Date: 2022-02-16 21:47:56.930183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6805441e9177'
down_revision = '51da8041d4ae'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
