"""seed data for brands, categories, products, reviews tables

Revision ID: e7a8050e3637
Revises: 2f100d842d26
Create Date: 2024-12-02 13:38:40.342310

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from uuid import uuid4
from datetime import datetime
import random
from faker import Faker

from services import BaseAuthService

from schemas import ProductStatus, ReviewStatus, UserType, DiscountType

# revision identifiers, used by Alembic.
revision: str = 'e7a8050e3637'
down_revision: Union[str, None] = '2f100d842d26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
fake = Faker()
service = BaseAuthService()

def get_brand_item(brand):
    return {
        "id": brand[0],
        "brand_name": brand[1],
        "description": fake.text(),
        "default_image_link": f"logo_{brand[1].lower()}",
        "dark_theme_image_link": f"logo_{brand[1].lower()}",
        "is_deleted": False,
        "created_at": datetime.utcnow()
    }

def get_category_item(category):
    return {
        "id": category[0],
        "category_name": category[1],
        "description": fake.text(),
        "is_deleted": False,
        "created_at": datetime.utcnow()
    }

def get_sub_category_item(category_id):
    return {
        "id": category_id,
        "sub_category_name": fake.company(),
        "description": fake.text(),
        "is_deleted": False,
        "created_at": datetime.utcnow()
    }

def get_product_item(product_id, brands, categories):
    return {
        "id": product_id,
        "brand_id": random.choice(brands)[0],
        "category_id": random.choice(categories)[0],
        "product_name": fake.text(max_nb_chars=50),
        "description": fake.text(),
        "price": round(random.uniform(50, 300), 2),
        "quantity": random.randint(1, 100),
        "main_image_link": fake.image_url(),
        "product_status": random.choice([ProductStatus.INVISIBLE, ProductStatus.VISIBLE]),
        "is_deleted": False,
        "created_at": datetime.utcnow()
    }

def get_user(user_id):
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = first_name.lower() + last_name + str(random.randint(1, 100))
    return {
        "id": user_id,
        "email": f"{username}@email.com",
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "password": service.get_password_hash("Pass@123"),
        "is_deleted": False,
        "user_type": UserType.USER,
        "created_at": datetime.utcnow(),
    }

def get_products_reviews(product_id, user_ids):
    return {
        "id": uuid4(),
        "product_id": product_id,
        "user_id": random.choice(user_ids),
        "content": fake.text(),
        "rating": random.randint(1, 5),
        "review_status": random.choice([ReviewStatus.INVISIBLE, ReviewStatus.VISIBLE]),
        "is_deleted": False,
        "created_at": datetime.utcnow()
    }

def get_discount_item(discount_id):
    return {
        "id": discount_id,
        "discount_name": fake.text(max_nb_chars=100),
        "description": fake.text(),
        "start_date": fake.date_this_month(before_today=True),
        "end_date": fake.date_this_year(before_today=False, after_today=True),
        "discount_type": random.choice([DiscountType.VALUE, DiscountType.PERCENTAGE]),
        "discount_value": round(random.uniform(10, 60), 2),
        "is_deleted": False,
        "created_at": datetime.utcnow()
    }

def get_product_discount_item(product_id, discount_ids):
    return {
        "id": uuid4(),
        "product_id": product_id,
        "discount_id": random.choice(discount_ids),
        "is_deleted": False,
        "created_at": datetime.utcnow()
    }


def get_product_sub_category_item(product_id, sub_category_ids):
    return {
        "id": uuid4(),
        "product_id": product_id,
        "sub_category_id": random.choice(sub_category_ids),
        "is_deleted": False,
        "created_at": datetime.utcnow()
    }

def upgrade() -> None:
    
    brands_table = table("brands",
        column('id', sa.UUID),
        column('brand_name', sa.String),
        column('description', sa.String),
        column('default_image_link', sa.String),
        column('dark_theme_image_link', sa.String),
        column('is_deleted', sa.Boolean),
        column('created_at', sa.DateTime),
    )

    categories_table = table("categories",
        column('id', sa.UUID),
        column('category_name', sa.String),
        column('description', sa.String),
        column('is_deleted', sa.Boolean),
        column('created_at', sa.DateTime)
    )

    sub_categories_table = table("sub_categories",
        column('id', sa.UUID),
        column('sub_category_name', sa.String),
        column('description', sa.String),
        column('is_deleted', sa.Boolean),
        column('created_at', sa.DateTime)
    )

    products_table = table("products",
        column('id', sa.UUID),
        column('brand_id', sa.UUID),
        column('category_id', sa.UUID),
        column('product_name', sa.String),
        column('description', sa.String),
        column('price', sa.Double),
        column('quantity', sa.Integer),
        column('main_image_link', sa.String),
        column('product_status', sa.Enum(ProductStatus)),
        column('is_deleted', sa.Boolean),
        column('created_at', sa.DateTime),
    )

    users_table = table("users",
        column('id', sa.UUID),
        column('email', sa.String),
        column('username', sa.String),
        column('first_name', sa.String),
        column('last_name', sa.String),
        column('password', sa.String),
        column('is_deleted', sa.Boolean),
        column('user_type', sa.Enum(UserType)),
        column('created_at', sa.DateTime),
    )

    reviews_table = table("reviews",
        column('id', sa.UUID),
        column('product_id', sa.UUID),
        column('user_id', sa.UUID),
        column('content', sa.String),
        column('rating', sa.Integer),
        column('review_status', sa.Enum(ReviewStatus)),
        column('is_deleted', sa.Boolean),
        column('created_at', sa.DateTime),
    )

    discounts_table = table("discounts",
        column('id', sa.UUID),
        column('discount_name', sa.String),
        column('description', sa.String),
        column('start_date', sa.DateTime),
        column('end_date', sa.DateTime),
        column('discount_type', sa.Enum(DiscountType)),
        column('discount_value', sa.Double),
        column('is_deleted', sa.Boolean),
        column('created_at', sa.DateTime)
    )
    
    products_discounts_table = table('products_discounts',
        column('id', sa.UUID),
        column('product_id', sa.UUID),
        column('discount_id', sa.UUID),
        column('is_deleted', sa.Boolean),
        column('created_at', sa.DateTime)
    )

    products_sub_categories_table = table('products_sub_categories',
        column('id', sa.UUID),
        column('product_id', sa.UUID),
        column('sub_category_id', sa.UUID),
        column('is_deleted', sa.Boolean),
        column('created_at', sa.DateTime)
    )

    brand_names = ['Sony', 'Samsung', 'Apple', 'Xiaomi', 'MSI', 'Oppo', 'Vivo', 'LG', 'Realme', 'HP', 'JBL', 'Asus', 'Acer', 'Lenovo']
    brands = [[uuid4(), brand_name] for brand_name in brand_names]
    op.bulk_insert(brands_table, [get_brand_item(brand) for brand in brands], multiinsert=False)

    number_of_categories, number_of_products, number_of_users, number_of_product_reviews, number_of_discounts, number_of_product_sub_categories = 5, 100, 10, 5, 100, 5
    categories = [[uuid4(), fake.company()] for index in range(number_of_categories)]
    op.bulk_insert(categories_table, [get_category_item(category) for category in categories], multiinsert=False)

    sub_category_ids = [uuid4() for index in range(number_of_categories)]
    op.bulk_insert(sub_categories_table, [get_sub_category_item(sub_category_id) for sub_category_id in sub_category_ids], multiinsert=False)

    product_ids = [uuid4() for index in range(number_of_products)]
    op.bulk_insert(products_table, [get_product_item(product_id, brands, categories) for product_id in product_ids], multiinsert=False)

    user_ids = [uuid4() for index in range(number_of_users)]
    op.bulk_insert(users_table, [get_user(user_id) for user_id in user_ids], multiinsert=False)

    for product_id in product_ids:
        op.bulk_insert(reviews_table, [get_products_reviews(product_id, user_ids) for i in range(number_of_product_reviews)], multiinsert=False)

    discount_ids = [uuid4() for index in range(number_of_discounts)]
    op.bulk_insert(discounts_table, [get_discount_item(discount_id) for discount_id in discount_ids], multiinsert=False)

    op.bulk_insert(products_discounts_table, [get_product_discount_item(product_id, discount_ids) for product_id in product_ids], multiinsert=False)
    
    for product_id in product_ids:
        op.bulk_insert(products_sub_categories_table, [get_product_sub_category_item(product_id, sub_category_ids) for i in range(number_of_product_sub_categories)], multiinsert=False)

def downgrade() -> None:
    pass
