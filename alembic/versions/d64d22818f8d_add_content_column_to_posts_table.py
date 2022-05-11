"""add content column to posts table

Revision ID: d64d22818f8d
Revises: a9d85183fbc1
Create Date: 2022-05-11 14:40:08.323051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd64d22818f8d'
down_revision = 'a9d85183fbc1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
