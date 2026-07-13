from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from bit_browser.models.base import APIModel


class ExtralogItem(APIModel):
    id: Optional[int] = None
    log_key: Optional[str] = None
    log_name: Optional[str] = None
    log_value: Optional[str] = None
    log_type: Optional[str] = None
    log_desc: Optional[str] = None
    log_remark: Optional[str] = None
    log_extra_info: Optional[str] = None
    created_time: Optional[str] = None


class ExtralogListData(APIModel):
    totalNum: int = 0
    list: List[ExtralogItem] = Field(default_factory=list)
