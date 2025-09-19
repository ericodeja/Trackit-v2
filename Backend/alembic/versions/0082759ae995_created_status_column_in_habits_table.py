"""Created status column in habits table

Revision ID: 0082759ae995
Revises: 70ce3b77ad31
Create Date: 2025-09-11 14:19:44.089769

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0082759ae995'
down_revision: Union[str, Sequence[str], None] = '70ce3b77ad31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the ENUM type first
    habit_status = sa.Enum("completed", "incomplete", name="habit_status")
    habit_status.create(op.get_bind())

    # Then add the column using that type
    op.add_column(
        'habits',
        sa.Column(
            'status',
            habit_status,
            nullable=False,
            server_default="incomplete"  # optional default
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the column first
    op.drop_column('habits', 'status')

    # Then drop the ENUM type
    sa.Enum(name="habit_status").drop(op.get_bind())
