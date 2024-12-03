from fastapi import Depends

from uuid import UUID

from schemas import Category

from .base import BaseRepository, InterfaceRepository

class CategoryRepository(BaseRepository, InterfaceRepository):

    def list(self, params):
        query = self.db.query(Category)
        query = self.filter(query, Category, params)
        query = self.search(query, Category, params)
        query = self.sort(query, Category, params)
        query = self.paginate(query, params)
        return query.all()
        
    def find_element_by_key(self, key: str, value: str, skip_filter: bool = False):
        return self.db.query(Category).execution_options(skip_visibility_filter=skip_filter).filter(getattr(Category, key) == value).first()