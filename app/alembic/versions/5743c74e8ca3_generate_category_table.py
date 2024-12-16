"""generate category table

Revision ID: 5743c74e8ca3
Revises: 4176e7b73ab8
Create Date: 2024-11-25 16:22:39.745967

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5743c74e8ca3'
down_revision: Union[str, None] = '4176e7b73ab8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    table = op.create_table(
        'categories',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('category_name', sa.String(100), unique=True, nullable=False),
        sa.Column('description', sa.String(255), nullable=False),
        sa.Column('icon', sa.String(50)),
        sa.Column('is_deleted', sa.Boolean, default=0),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('deleted_at', sa.DateTime)
    )

def downgrade() -> None:
    op.drop_table('categories')
