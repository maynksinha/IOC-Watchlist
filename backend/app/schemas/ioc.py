from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.constants import MAX_VALUE_LENGTH, MAX_NOTE_LENGTH, MAX_TAGS, MAX_TAG_LENGTH


class IOCCreate(BaseModel):
    value: str = Field(..., min_length=1, max_length=MAX_VALUE_LENGTH)
    note: Optional[str] = Field(default=None, max_length=MAX_NOTE_LENGTH)
    tags: list[str] = Field(default_factory=list, max_length=MAX_TAGS)

    @field_validator("value")
    @classmethod
    def value_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("value must not be empty")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: list[str]) -> list[str]:
        cleaned: list[str] = []
        for tag in v:
            tag = tag.strip()
            if not tag:
                continue
            if len(tag) > MAX_TAG_LENGTH:
                raise ValueError(f"each tag must be at most {MAX_TAG_LENGTH} characters")
            cleaned.append(tag)
        return cleaned
