"""Updated relationships with cascade delete

Revision ID: 59fae82b7a28
Revises: f8a764dd6c75
Create Date: 2025-09-11 00:56:48.039744
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "59fae82b7a28"
down_revision: Union[str, Sequence[str], None] = "f8a764dd6c75"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema with cascade delete on user_id FKs."""
    # Habits → Users
    op.drop_constraint("habits_user_id_fkey", "habits", type_="foreignkey")
    op.create_foreign_key(
        "fk_habits_user_id", "habits", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )

    # Profile changes → Users
    op.drop_constraint("profile_changes_user_id_fkey", "profile_changes", type_="foreignkey")
    op.create_foreign_key(
        "fk_profile_changes_user_id", "profile_changes", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )

    # Tokens → Users
    op.drop_constraint("tokens_user_id_fkey", "tokens", type_="foreignkey")
    op.create_foreign_key(
        "fk_tokens_user_id", "tokens", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    """Downgrade schema by removing cascade deletes."""
    # Tokens → Users
    op.drop_constraint("fk_tokens_user_id", "tokens", type_="foreignkey")
    op.create_foreign_key("tokens_user_id_fkey", "tokens", "users", ["user_id"], ["id"])

    # Profile changes → Users
    op.drop_constraint("fk_profile_changes_user_id", "profile_changes", type_="foreignkey")
    op.create_foreign_key("profile_changes_user_id_fkey", "profile_changes", "users", ["user_id"], ["id"])

    # Habits → Users
    op.drop_constraint("fk_habits_user_id", "habits", type_="foreignkey")
    op.create_foreign_key("habits_user_id_fkey", "habits", "users", ["user_id"], ["id"])
