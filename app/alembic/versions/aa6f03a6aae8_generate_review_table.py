"""generate review table

Revision ID: aa6f03a6aae8
Revises: a078898a5ae9
Create Date: 2024-12-02 15:21:41.315519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from schemas import ReviewStatus

# revision identifiers, used by Alembic.
revision: str = 'aa6f03a6aae8'
down_revision: Union[str, None] = 'a078898a5ae9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    table = op.create_table(
        'reviews',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('product_id', sa.UUID, nullable=False),
        sa.Column('user_id', sa.UUID, nullable=False),
        sa.Column('content', sa.String(255), nullable=False),
        sa.Column('rating', sa.Integer, default=5),
        sa.Column('review_status', sa.Enum(ReviewStatus), default=ReviewStatus.INVISIBLE),
        sa.Column('is_deleted', sa.Boolean, default=0),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('deleted_at', sa.DateTime)
    )
    op.create_foreign_key('fk_review_product', 'reviews', 'products', ['product_id'], ['id'])
    op.create_foreign_key('fk_review_user', 'reviews', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    op.drop_table('reviews')
    op.execute('DROP TYPE reviewstatus;')