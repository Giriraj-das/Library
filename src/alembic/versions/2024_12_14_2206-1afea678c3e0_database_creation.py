"""Database creation

Revision ID: 1afea678c3e0
Revises: 
Create Date: 2024-12-14 22:06:00.463007

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1afea678c3e0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "authors",
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_authors")),
    )
    op.create_table(
        "books",
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column(
            "available_copies",
            sa.Integer(),
            server_default="1",
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["authors.id"],
            name=op.f("fk_books_author_id_authors"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_books")),
    )
    op.create_table(
        "borrows",
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("borrower_name", sa.String(), nullable=False),
        sa.Column(
            "borrow_date",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("return_date", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["book_id"], ["books.id"], name=op.f("fk_borrows_book_id_books")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_borrows")),
    )


def downgrade() -> None:
    op.drop_table("borrows")
    op.drop_table("books")
    op.drop_table("authors")
