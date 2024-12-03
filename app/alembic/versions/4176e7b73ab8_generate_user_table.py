"""generate user table

Revision ID: 4176e7b73ab8
Revises: 
Create Date: 2024-11-25 16:13:20.926001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from schemas import UserType

from datetime import datetime
from uuid import uuid4

from services import BaseAuthService
from config import ADMIN_DEFAULT_PASSWORD


# revision identifiers, used by Alembic.
revision: str = '4176e7b73ab8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

service = BaseAuthService()

def upgrade() -> None:
    table = op.create_table(
        'users',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('username', sa.String(255), unique=True, nullable=False),
        sa.Column('first_name', sa.String(255), nullable=False),
        sa.Column('last_name', sa.String(255), nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('is_deleted', sa.Boolean, default=0),
        sa.Column('user_type', sa.Enum(UserType), default=UserType.USER),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('deleted_at', sa.DateTime)
    )

    op.bulk_insert(table, [
        {
            "id": uuid4(),
            "email": "admin@email.com",
            "username": "admin",
            "first_name": "System",
            "last_name": "Admin",
            "password": service.get_password_hash(ADMIN_DEFAULT_PASSWORD),
            "is_deleted": False,
            "user_type": UserType.ADMIN,
            "created_at": datetime.utcnow(),
        }
    ])


def downgrade() -> None:
    op.drop_table('users')
    op.execute('DROP TYPE usertype;')
