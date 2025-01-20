"""att. tab novelist

Revision ID: c692f2155ba1
Revises: f2b2ff9347e6
Create Date: 2025-01-20 17:17:21.348826

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c692f2155ba1'
down_revision: Union[str, None] = 'f2b2ff9347e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
