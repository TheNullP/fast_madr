"""adicionando caminho para foto de perfil

Revision ID: 2100d87b4995
Revises: 7aababcf0d93
Create Date: 2025-03-03 17:36:02.074361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2100d87b4995'
down_revision: Union[str, None] = '7aababcf0d93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
