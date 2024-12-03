from fastapi import Depends
from sqlalchemy import func, case, distinct
from uuid import UUID
from datetime import datetime
from schemas import Product, Brand, Category, Review, Discount, ProductDiscount, DiscountType, ProductSubCategory, SubCategory

from .base import BaseRepository, InterfaceRepository

class ProductRepository(BaseRepository, InterfaceRepository):

    def get_table_query(self):
        discounts_cte = self.get_discounts_cte()
        sub_categories_cte = self.get_sub_categories_cte()
        return self.db.query(
            Product.id
            , Product.product_name
            , Product.description
            , Product.price
            , Product.quantity
            , Product.main_image_link
            , Product.image_links
            , Product.product_status
            , Brand.brand_name
            , Category.category_name
            , discounts_cte.c.discount_type
        ).join(Product.brand, isouter=True
        ).join(Product.category, isouter=True
        ).join(ProductSubCategory, ProductSubCategory.product_id == Product.id, isouter=True
        ).join(SubCategory, SubCategory.id == ProductSubCategory.sub_category_id, isouter=True
        ).join(sub_categories_cte, sub_categories_cte.c.product_id == Product.id, isouter=True
        ).join(discounts_cte, discounts_cte.c.product_id == Product.id and discounts_cte.c.row_number == 1, isouter=True
        ).join(Review, Review.product_id == Product.id, isouter=True
        ).add_column((func.array_agg(sub_categories_cte.c.sub_category.distinct())).label("sub_categories")
        ).add_column((func.sum(Review.rating)/func.count(Review.id)).label("average_rating")
        ).add_column((case(
            (discounts_cte.c.discount_type == DiscountType.PERCENTAGE, discounts_cte.c.discount_value*Product.price/100),
            else_=(discounts_cte.c.discount_value),
        )).label("discount_value")
                ).add_column((case(
            (discounts_cte.c.discount_type == DiscountType.VALUE, (discounts_cte.c.discount_value/Product.price)*100),
            else_=(discounts_cte.c.discount_value),
        )).label("discount_percentage")
        ).add_column((case(
            (discounts_cte.c.discount_type == DiscountType.PERCENTAGE, (100-discounts_cte.c.discount_value)*Product.price/100),
            else_=(Product.price - discounts_cte.c.discount_value),
        )).label("final_price")
        ).group_by(
            Product.id
            , Product.product_name
            , Product.description
            , Product.price
            , Product.quantity
            , Product.main_image_link
            , Product.image_links
            , Product.product_status
            , Brand.brand_name
            , Category.category_name
            , discounts_cte.c.discount_type
            , "discount_value"
            , "discount_percentage"
        )

    def get_discounts_cte(self):
        today = datetime.today().strftime('%Y-%m-%d')
        return self.db.query(
            ProductDiscount.product_id
            , Discount.discount_type
            , Discount.discount_value
        ).join(ProductDiscount, Discount.id == ProductDiscount.discount_id and (Discount.start_date <= today, Discount.end_date >= today), isouter=True
        ).add_column((func.row_number().over(partition_by=ProductDiscount.product_id, order_by=[Discount.start_date, Discount.end_date])).label("row_number")
        ).cte("discounts_cte")

    def get_sub_categories_cte(self):
        return self.db.query(
            ProductSubCategory.product_id
            , SubCategory.sub_category_name
        ).join(SubCategory, SubCategory.id == ProductSubCategory.sub_category_id, isouter=True
        ).add_column((SubCategory.sub_category_name + " - " + SubCategory.description).label("sub_category")
        ).cte("sub_categories_cte")

    def list(self, params):
        query = self.get_table_query()
        query = self.filter(query, Product, params)
        query = self.search(query, Product, params)
        query = self.sort(query, Product, params)
        query = self.paginate(query, params)
        return query.all()
        
    def find_element_by_key(self, key: str, value: str, skip_filter: bool = False):
        return self.get_table_query().execution_options(skip_visibility_filter=skip_filter).filter(getattr(Product, key) == value).first()