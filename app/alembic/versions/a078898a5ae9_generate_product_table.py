"""generate product table

Revision ID: a078898a5ae9
Revises: 96fe0ab386f4
Create Date: 2024-11-28 11:47:00.590410

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from schemas import ProductStatus

# revision identifiers, used by Alembic.
revision: str = 'a078898a5ae9'
down_revision: Union[str, None] = '96fe0ab386f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    table = op.create_table(
        'products',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('brand_id', sa.UUID, nullable=False),
        sa.Column('category_id', sa.UUID, nullable=False),
        sa.Column('product_name', sa.String(100), unique=True, nullable=False),
        sa.Column('description', sa.String(255), nullable=False),
        sa.Column('price', sa.Double, nullable=False),
        sa.Column('quantity', sa.Integer, default=0),
        sa.Column('main_image_link', sa.String(100)),
        sa.Column('image_links', sa.String(255)),
        sa.Column('product_status', sa.Enum(ProductStatus), default=ProductStatus.INVISIBLE),
        sa.Column('is_deleted', sa.Boolean, default=0),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('deleted_at', sa.DateTime)
    )
    op.create_foreign_key('fk_product_brand', 'products', 'brands', ['brand_id'], ['id'])
    op.create_foreign_key('fk_product_category', 'products', 'categories', ['category_id'], ['id'])

def downgrade() -> None:
    op.drop_table('products')
    op.execute('DROP TYPE productstatus;')
