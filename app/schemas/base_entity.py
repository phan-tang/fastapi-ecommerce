from sqlalchemy import Column, Uuid, Boolean, DateTime, event
from sqlalchemy.orm import ORMExecuteState, with_loader_criteria
from database import LocalSession
import uuid

class BaseEntity:
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

@event.listens_for(LocalSession, "do_orm_execute")
def _add_filtering_criteria(execute_state: ORMExecuteState):
    skip_filter = execute_state.execution_options.get("skip_visibility_filter", False)
    if execute_state.is_select and not skip_filter:
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                BaseEntity,
                lambda cls: cls.is_deleted.is_(False),
                include_aliases=True,
            )
        )