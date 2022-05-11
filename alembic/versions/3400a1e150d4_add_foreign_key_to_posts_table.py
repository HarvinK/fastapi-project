"""add foreign key to posts table

Revision ID: 3400a1e150d4
Revises: 4cbb34e24e8b
Create Date: 2022-05-11 14:57:51.364984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3400a1e150d4'
down_revision = '4cbb34e24e8b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk',
                            source_table="posts",
                            referent_table="users",
                            local_cols=['owner_id'], #id field in posts table
                            remote_cols=['id'], #id field in users table
                            ondelete="CASCADE"
                            )
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
