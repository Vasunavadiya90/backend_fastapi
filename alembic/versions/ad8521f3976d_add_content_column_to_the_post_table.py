"""add content column to the post table

Revision ID: ad8521f3976d
Revises: 0201c9f057f4
Create Date: 2026-11-23 12:05:38.998116

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad8521f3976d'
down_revision: Union[str, Sequence[str], None] = '0201c9f057f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content', sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
