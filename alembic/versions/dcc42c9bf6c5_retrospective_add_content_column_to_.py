"""retrospective: add content column to posts table

Revision ID: dcc42c9bf6c5
Revises: 9f8a99e22a6a
Create Date: 2025-02-11 15:14:53.206120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dcc42c9bf6c5'
down_revision: Union[str, None] = '9f8a99e22a6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
