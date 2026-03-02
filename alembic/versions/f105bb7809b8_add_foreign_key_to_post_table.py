"""add foreign key to post table

Revision ID: f105bb7809b8
Revises: ece2a0329fa7
Create Date: 2026-03-02 00:57:12.377922

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f105bb7809b8'
down_revision: Union[str, Sequence[str], None] = 'ece2a0329fa7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. add column with temporary default
    op.add_column(
        "posts",
        sa.Column("owner_id", sa.Integer(), nullable=False, server_default="1")
    )

    # 2. add foreign key
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )

    # 3. remove default (important)
    op.alter_column("posts", "owner_id", server_default=None)


def downgrade():
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    