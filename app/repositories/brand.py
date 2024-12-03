from uuid import UUID

from schemas import Brand

from .base import BaseRepository, InterfaceRepository

class BrandRepository(BaseRepository, InterfaceRepository):
    
    def list(self, params):
        query = self.db.query(Brand)
        query = self.filter(query, Brand, params)
        query = self.search(query, Brand, params)
        query = self.sort(query, Brand, params)
        query = self.paginate(query, params)
        return query.all()
        
    def find_element_by_key(self, key: str, value: str, skip_filter: bool = False):
        return self.db.query(Brand).execution_options(skip_visibility_filter=skip_filter).filter(getattr(Brand, key) == value).first()