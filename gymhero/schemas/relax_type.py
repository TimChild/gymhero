import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class RelaxTypeBase(BaseModel):
    name: str


class RelaxTypeCreate(RelaxTypeBase):
    pass


class RelaxTypeUpdate(RelaxTypeBase):
    name: Optional[str] = None


class RelaxTypeInDB(RelaxTypeBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)


class RelaxTypeOut(RelaxTypeBase):
    id: int
    name: str
