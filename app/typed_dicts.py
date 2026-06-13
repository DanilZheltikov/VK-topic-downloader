from typing import TypedDict


class TopicWithIDDict(TypedDict):
    id: int
    title: str
    comments: int


class Comment(TypedDict):
    date: int
    text: str


class Topic(TypedDict):
    title: str
    comments: list[Comment]
