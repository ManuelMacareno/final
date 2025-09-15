from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declarative_base, declared_attr


class BaseMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


Base = declarative_base(cls=BaseMixin)