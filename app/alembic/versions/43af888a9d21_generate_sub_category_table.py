"""generate sub_sub_category table

Revision ID: 43af888a9d21
Revises: 906d79fc5f6c
Create Date: 2024-12-02 21:35:40.512760

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43af888a9d21'
down_revision: Union[str, None] = '906d79fc5f6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        table = op.create_table(
        'sub_categories',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('sub_category_name', sa.String(100), unique=True, nullable=False),
        sa.Column('description', sa.String(255), nullable=False),
        sa.Column('is_deleted', sa.Boolean, default=0),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('deleted_at', sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table('sub_categories')
