"""add foreign key to the posts table

Revision ID: 4ccc0680e64b
Revises: 76b2a7d1024d
Create Date: 2026-11-23 12:24:03.956356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ccc0680e64b'
down_revision: Union[str, Sequence[str], None] = '76b2a7d1024d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('owner_id', sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk', 
                          source_table="posts",
                          referent_table="users",
                          local_cols=['owner_id'], 
                          remote_cols=['id'],
                          ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts','owner_id')
    pass
