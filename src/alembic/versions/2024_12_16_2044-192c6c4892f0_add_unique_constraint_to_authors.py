"""Add unique constraint to authors

Revision ID: 192c6c4892f0
Revises: 1afea678c3e0
Create Date: 2024-12-16 20:44:29.467247

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "192c6c4892f0"
down_revision: Union[str, None] = "1afea678c3e0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        op.f("uq_authors_first_name_last_name"),
        "authors",
        ["first_name", "last_name"],
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("uq_authors_first_name_last_name"), "authors", type_="unique"
    )
