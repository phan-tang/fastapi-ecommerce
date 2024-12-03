"""generate products_discounts table

Revision ID: 906d79fc5f6c
Revises: aa6f03a6aae8
Create Date: 2024-12-02 17:59:35.778152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '906d79fc5f6c'
down_revision: Union[str, None] = 'aa6f03a6aae8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    table = op.create_table(
        'products_discounts',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('product_id', sa.UUID, nullable=False),
        sa.Column('discount_id', sa.UUID, nullable=False),
        sa.Column('is_deleted', sa.Boolean, default=0),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('deleted_at', sa.DateTime)
    )
    op.create_foreign_key('fk_product_discount_product', 'products_discounts', 'products', ['product_id'], ['id'])
    op.create_foreign_key('fk_product_discount_discount', 'products_discounts', 'discounts', ['discount_id'], ['id'])


def downgrade() -> None:
    op.drop_table('products_discounts')
