"""Add user_id to Subject model

Revision ID: 7789bd1ebb7c
Revises: 7486967a48ab
Create Date: 2023-12-21 09:32:42.649328

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7789bd1ebb7c'
down_revision: Union[str, None] = '7486967a48ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###