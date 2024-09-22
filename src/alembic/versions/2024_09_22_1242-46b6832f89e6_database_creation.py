"""Database creation

Revision ID: 46b6832f89e6
Revises: 
Create Date: 2024-09-22 12:42:00.153886

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "46b6832f89e6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column(
            "status",
            sa.Enum(
                "в процессе",
                "отправлен",
                "доставлен",
                name="order_status_enum",
            ),
            server_default="в процессе",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_orders")),
    )
    op.create_table(
        "products",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column(
            "stock_quantity", sa.Integer(), server_default="0", nullable=False
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_products")),
    )
    op.create_table(
        "order_item",
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column(
            "quantity", sa.Integer(), server_default="1", nullable=False
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
            name=op.f("fk_order_item_order_id_orders"),
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name=op.f("fk_order_item_product_id_products"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_order_item")),
        sa.UniqueConstraint(
            "order_id",
            "product_id",
            name=op.f("uq_order_item_order_id_product_id"),
        ),
    )


def downgrade() -> None:
    op.drop_table("order_item")
    op.drop_table("products")
    op.drop_table("orders")
