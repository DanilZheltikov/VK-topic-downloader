from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, PlainSerializer


class Comments(BaseModel):
    date: Annotated[
        datetime,
        PlainSerializer(
            func=lambda date: date.strftime('%d.%m.%Y'),
            return_type=str
        )
    ]
    text: str

    @field_validator('date', mode='before')
    @classmethod
    def date_from_timestamp(cls, value: int | datetime) -> datetime:
        """VK API возвращает date как Unix timestamp (int)."""
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        return value


class Topic(BaseModel):
    title: str
    comments: list[Comments]
