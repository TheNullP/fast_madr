"""atualizado o campo profile_picture, para poder ser nulo

Revision ID: db92803d0ac5
Revises: 2100d87b4995
Create Date: 2025-03-03 18:10:51.871833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db92803d0ac5'
down_revision: Union[str, None] = '2100d87b4995'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
