"""retrospective: create a post table

Revision ID: 9f8a99e22a6a
Revises: 
Create Date: 2025-02-11 15:03:42.438007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f8a99e22a6a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None: # This function defines the logic for you to upgrade your database and add incremental changes to it.
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None: # This function defines the logic to rollback changes to the database. Whatever you define in upgrade, you must provide the logic to undo those changes in downgrade
    op.drop_table('posts')
