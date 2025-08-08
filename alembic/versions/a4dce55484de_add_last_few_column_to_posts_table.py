"""add last few column to posts table

Revision ID: a4dce55484de
Revises: bb195aaac9a0
Create Date: 2025-08-05 23:25:20.454017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4dce55484de'
down_revision: Union[str, Sequence[str], None] = 'bb195aaac9a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column(
            'published', 
            sa.Boolean(), 
            nullable=False, 
            server_default=sa.text('TRUE')  # ✅ 正确用法
        )
    )
    op.add_column(
        'posts',
        sa.Column(
            'created_at', 
            sa.TIMESTAMP(timezone=True), 
            nullable=False, 
            server_default=sa.text('NOW()')  # ✅ 一定要是函数形式 NOW()
        )
    )
    pass

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'created_at')   # ⚠️ 注意顺序：必须先删 created_at
    op.drop_column('posts', 'published')    # 然后才能删 published
    pass
