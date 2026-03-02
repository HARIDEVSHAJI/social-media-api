"""add content coulumn to post table

Revision ID: b6aed8b93e6e
Revises: 390a8bce268e
Create Date: 2026-03-02 00:32:21.030790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6aed8b93e6e'
down_revision: Union[str, Sequence[str], None] = '390a8bce268e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column("content", sa.String(), nullable=False)
    )
    pass


def downgrade():
    op.drop_column("posts", "content")