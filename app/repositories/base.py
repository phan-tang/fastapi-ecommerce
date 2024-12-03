from abc import ABC, abstractmethod
from fastapi import Depends
from sqlalchemy import desc, or_, and_, func
from sqlalchemy.orm import Session

from config import NOT_FILTER_FIELDS
from database import get_db_session, LocalSession
from schemas import BaseEntity

from schemas import Brand

class BaseRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_session)) -> None:
        self.db = db

    def create(self, item):
        self.db.add(item)
        self.db.commit()
        return item

    def update(self, item):
        self.db.merge(item)
        self.db.commit()
        return item

    def delete(self, item):
        self.db.delete(item)
        self.db.commit()
        return "Delete this item successfully"

    def soft_delete(self, item):
        self.db.merge(item)
        self.db.commit()
        return "Delete this item successfully"

    def paginate(self, query, params):
        if params["paginate"] != "all":
            return query.offset((params["page"]-1)*int(params["paginate"])).limit(int(params["paginate"]))
        return query

    def sort(self, query, model, params):
        sort_attribute = self.get_sort_attribute(params['sort'], model)
        if params["order"] == "desc":
            return query.order_by(desc(sort_attribute))
        return query.order_by(sort_attribute)

    def get_sort_attribute(self, params_sort, model):
        model = model if params_sort['use_main_model'] else params_sort["model"]
        return getattr(model, params_sort["field"]) if model else params_sort["field"]

    def search(self, query, model, params):
        if params['search']['value'] is None:
            return query
        search_args = [func.lower(getattr(model, field)).like(f"%{params['search']['value'].lower()}%")
                       for field in params['search']['fields']]
        return query.filter(or_(*search_args))

    def filter(self, query, model, params):
        filters_args = [self.get_filter_attribute(key, params, model).in_(params[key]['values']) for key in params if self.check_execute_filter(params, key)]
        return query.filter(and_(*filters_args))
    
    def check_execute_filter(self, params, key):
        return key not in NOT_FILTER_FIELDS and params[key] is not None and params[key]["values"] is not None

    def get_filter_attribute(self, key, params, model):
        used_model = model if params[key]['use_main_model'] else params[key]['model']
        return getattr(used_model, key) if used_model else key

class InterfaceRepository(ABC):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def find_element_by_key(self, key, value, skip_filter):
        pass

    @abstractmethod
    def create(self, item):
        pass

    @abstractmethod
    def update(self, item):
        pass

    @abstractmethod
    def delete(self, item):
        pass

    @abstractmethod
    def paginate(self, query, params):
        pass
