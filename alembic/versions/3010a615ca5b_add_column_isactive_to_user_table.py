"""add column isactive to user table

Revision ID: 3010a615ca5b
Revises: 24a8e355b39d
Create Date: 2024-04-29 09:46:01.062769

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3010a615ca5b'
down_revision: Union[str, None] = '24a8e355b39d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
