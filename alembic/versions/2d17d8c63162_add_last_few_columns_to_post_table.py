"""add last few columns to post table

Revision ID: 2d17d8c63162
Revises: f105bb7809b8
Create Date: 2026-03-02 01:07:16.451809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d17d8c63162'
down_revision: Union[str, Sequence[str], None] = 'f105bb7809b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column(
            "published",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("TRUE"),
        ),
    )

    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )


def downgrade():
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")