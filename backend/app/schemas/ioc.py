from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from .tag import TagSchema


class IOCCreate(BaseModel):
    value: str
    note: Optional[str] = None
    tags: list[str] = []

    @field_validator("value")
    @classmethod
    def value_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("value must not be empty")
        return v


class IOCResponse(BaseModel):
    id: int
    ioc_type: str
    ioc_raw: str
    ioc_canonical: str
    note: Optional[str]
    tags: list[TagSchema]
    created_at: datetime

    model_config = {"from_attributes": True}


class IOCListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: list[IOCResponse]
