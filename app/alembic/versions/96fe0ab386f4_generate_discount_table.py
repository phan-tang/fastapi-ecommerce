"""generate discount table

Revision ID: 96fe0ab386f4
Revises: ce85d6bdff93
Create Date: 2024-11-28 11:46:36.897209

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from schemas import DiscountType

# revision identifiers, used by Alembic.
revision: str = '96fe0ab386f4'
down_revision: Union[str, None] = 'ce85d6bdff93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    table = op.create_table(
        'discounts',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('discount_name', sa.String(100), nullable=False),
        sa.Column('description', sa.String(255), nullable=False),
        sa.Column('start_date', sa.DateTime, nullable=False),
        sa.Column('end_date', sa.DateTime),
        sa.Column('discount_type', sa.Enum(DiscountType), default=DiscountType.VALUE),
        sa.Column('discount_value', sa.Double, nullable=False),
        sa.Column('is_deleted', sa.Boolean, default=0),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('deleted_at', sa.DateTime)
    )

def downgrade() -> None:
    op.drop_table('discounts')
    op.execute('DROP TYPE discounttype;')