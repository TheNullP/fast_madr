"""adiciona novo campo file_book na tabela book

Revision ID: 7216ae07d82c
Revises: db92803d0ac5
Create Date: 2025-04-25 20:51:06.839340

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7216ae07d82c'
down_revision: Union[str, None] = 'db92803d0ac5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
