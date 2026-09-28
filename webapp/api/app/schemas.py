"""Pydantic request/response models for the lists API."""

from pydantic import BaseModel, Field


class ListSummary(BaseModel):
    name: str
    item_count: int


class ListItemsPage(BaseModel):
    items: list[str]
    total: int
    page: int
    page_size: int


class CreateListRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class AddItemRequest(BaseModel):
    domain: str = Field(min_length=1, max_length=253)
