"""generate brand table

Revision ID: ce85d6bdff93
Revises: 5743c74e8ca3
Create Date: 2024-11-27 18:06:39.626964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'ce85d6bdff93'
down_revision: Union[str, None] = '5743c74e8ca3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    table = op.create_table(
        'brands',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('brand_name', sa.String(100), unique=True, nullable=False),
        sa.Column('description', sa.String(255), nullable=False),
        sa.Column('default_image_link', sa.String(255)),
        sa.Column('dark_theme_image_link', sa.String(255)),
        sa.Column('is_deleted', sa.Boolean, default=0),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('deleted_at', sa.DateTime)
    )
    
def downgrade() -> None:
    op.drop_table('brands')
