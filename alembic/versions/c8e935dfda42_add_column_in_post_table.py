"""add column in post table

Revision ID: c8e935dfda42
Revises: 4fc694219a5c
Create Date: 2025-08-05 23:00:16.735708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8e935dfda42'
down_revision: Union[str, Sequence[str], None] = '4fc694219a5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts', 
        sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
