from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from gymhero.database.base_class import Base


class Relax(Base):
    __tablename__ = "relax"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    relax_type_id = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )


class RelaxType(Base):
    __tablename__ = "relax_types"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self):
        return f"RelaxType -- created_at={self.created_at}"
