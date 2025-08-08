"""add user table

Revision ID: 54c098e77151
Revises: c8e935dfda42
Create Date: 2025-08-05 23:06:47.031499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54c098e77151'
down_revision: Union[str, Sequence[str], None] = 'c8e935dfda42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),  
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('now()'),nullable=False),
                  sa.PrimaryKeyConstraint('id'),
                  sa.UniqueConstraint('email')
        )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")

    pass
