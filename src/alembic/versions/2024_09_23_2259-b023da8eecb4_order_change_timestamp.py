"""Order change TIMESTAMP

Revision ID: b023da8eecb4
Revises: 46b6832f89e6
Create Date: 2024-09-23 22:59:01.395194

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b023da8eecb4"
down_revision: Union[str, None] = "46b6832f89e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "orders",
        "created_at",
        existing_type=sa.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )


def downgrade() -> None:
    op.alter_column(
        "orders",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=sa.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
