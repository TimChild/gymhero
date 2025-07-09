import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class RelaxBase(BaseModel):
    name: str
    description: Optional[str] = None


class RelaxCreate(RelaxBase):
    relax_type_id: int


class RelaxUpdate(RelaxBase):
    name: Optional[str] = None
    description: Optional[str] = None
    relax_type_id: Optional[int] = None


class RelaxInDB(RelaxBase):
    id: int
    relax_type_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)


class RelaxOut(RelaxBase):
    id: int
    name: str
    description: Optional[str] = None
