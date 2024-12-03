from uuid import UUID

from schemas import User

from .base import BaseRepository, InterfaceRepository

class UserRepository(BaseRepository, InterfaceRepository):
    
    def list(self, params):
        query = self.db.query(User)
        query = self.filter(query, User, params)
        query = self.search(query, User, params)
        query = self.sort(query, User, params)
        query = self.paginate(query, params)
        return query.all()

    def find_element_by_key(self, key: str, value: str, skip_filter: bool = False):
        return self.db.query(User).execution_options(skip_visibility_filter=skip_filter).filter(getattr(User, key) == value).first()