"""Database creation

Revision ID: 1fdf90e4360a
Revises: 
Create Date: 2024-12-18 16:29:32.938844

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1fdf90e4360a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "authors",
        sa.Column("first_name", sa.String(length=15), nullable=False),
        sa.Column("last_name", sa.String(length=50), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_authors")),
        sa.UniqueConstraint(
            "first_name",
            "last_name",
            name=op.f("uq_authors_first_name_last_name"),
        ),
    )
    op.create_table(
        "books",
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
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
