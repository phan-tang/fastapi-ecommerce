from fastapi import Depends

from uuid import UUID

from schemas import Review, User

from .base import BaseRepository, InterfaceRepository

class ReviewRepository(BaseRepository, InterfaceRepository):

    def get_table_query(self):
        return self.db.query(
            Review.id
            , Review.product_id
            , Review.user_id
            , Review.content
            , Review.rating
            , Review.review_status
            , Review.is_deleted
            , Review.created_at
            , Review.updated_at
            , User.email
            ).add_column((User.first_name + ' ' + User.last_name).label('full_name')).join(Review.user)

    def list(self, params):
        query = self.get_table_query()
        query = self.filter(query, Review, params)
        query = self.search(query, Review, params)
        query = self.sort(query, Review, params)
        query = self.paginate(query, params)
        return query.all()
        
    def find_element_by_key(self, key: str, value: str, skip_filter: bool = False):
        return self.get_table_query().execution_options(skip_visibility_filter=skip_filter).filter(getattr(Review, key) == value).first()