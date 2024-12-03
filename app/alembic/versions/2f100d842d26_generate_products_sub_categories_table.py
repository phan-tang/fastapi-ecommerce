"""generate products_sub_categories table

Revision ID: 2f100d842d26
Revises: 43af888a9d21
Create Date: 2024-12-02 21:36:08.199798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f100d842d26'
down_revision: Union[str, None] = '43af888a9d21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    table = op.create_table(
        'products_sub_categories',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('product_id', sa.UUID, nullable=False),
        sa.Column('sub_category_id', sa.UUID, nullable=False),
        sa.Column('is_deleted', sa.Boolean, default=0),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('deleted_at', sa.DateTime)
    )
    op.create_foreign_key('fk_product_sub_category_product', 'products_sub_categories', 'products', ['product_id'], ['id'])
    op.create_foreign_key('fk_product_sub_category_sub_category', 'products_sub_categories', 'sub_categories', ['sub_category_id'], ['id'])


def downgrade() -> None:
    op.drop_table('products_sub_categories')
