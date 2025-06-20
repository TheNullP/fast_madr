"""att. tab book

Revision ID: dac50c7f4aae
Revises: c692f2155ba1
Create Date: 2025-01-20 18:28:07.373096

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dac50c7f4aae'
down_revision: Union[str, None] = 'c692f2155ba1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on = '434d09a7f751'



def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('id_author', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'books', 'novelists', ['id_author'], ['id'])
    op.alter_column('novelists', 'nome',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('novelists', 'nome',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.drop_column('books', 'id_author')
    # ### end Alembic commands ###
