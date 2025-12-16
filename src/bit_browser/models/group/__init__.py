from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from bit_browser.models.base import APIModel


class Group(APIModel):
    id: str
    groupName: str
    sortNum: Optional[int] = None


class GroupListData(APIModel):
    totalNum: int = 0
    list: List[Group] = Field(default_factory=list)
