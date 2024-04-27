"""add content column to posts table

Revision ID: 90aa9fa8e7e5
Revises: 8b17bc13eee5
Create Date: 2024-04-27 14:14:11.635059

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90aa9fa8e7e5'
down_revision: Union[str, None] = '8b17bc13eee5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content',sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
