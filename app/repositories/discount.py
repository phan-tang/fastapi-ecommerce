from fastapi import Depends

from uuid import UUID

from schemas import Discount

from .base import BaseRepository, InterfaceRepository

class DiscountRepository(BaseRepository, InterfaceRepository):

    def list(self, params):
        query = self.db.query(Discount)
        query = self.filter(query, Discount, params)
        query = self.search(query, Discount, params)
        query = self.sort(query, Discount, params)
        query = self.paginate(query, params)
        return query.all()
        
    def find_element_by_key(self, key: str, value: str, skip_filter: bool = False):
        return self.db.query(Discount).execution_options(skip_visibility_filter=skip_filter).filter(getattr(Discount, key) == value).first()