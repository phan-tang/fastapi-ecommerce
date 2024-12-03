from fastapi import Depends

from uuid import UUID

from schemas import SubCategory

from .base import BaseRepository, InterfaceRepository

class SubCategoryRepository(BaseRepository, InterfaceRepository):

    def list(self, params):
        query = self.db.query(SubCategory)
        query = self.filter(query, SubCategory, params)
        query = self.search(query, SubCategory, params)
        query = self.sort(query, SubCategory, params)
        query = self.paginate(query, params)
        return query.all()
        
    def find_element_by_key(self, key: str, value: str, skip_filter: bool = False):
        return self.db.query(SubCategory).execution_options(skip_visibility_filter=skip_filter).filter(getattr(SubCategory, key) == value).first()