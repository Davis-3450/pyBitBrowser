from __future__ import annotations

from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

PYDANTIC_V2 = hasattr(BaseModel, "model_validate")

T = TypeVar("T")

if PYDANTIC_V2:
    from pydantic import ConfigDict

    class APIModel(BaseModel):
        model_config = ConfigDict(populate_by_name=True, extra="allow")

    class APIResponse(BaseModel, Generic[T]):
        model_config = ConfigDict(populate_by_name=True, extra="allow")

        success: bool
        msg: Optional[str] = None
        data: Optional[T] = None

else:
    from pydantic.generics import GenericModel

    class APIModel(BaseModel):
        class Config:  # noqa: D106
            allow_population_by_field_name = True
            extra = "allow"

    class APIResponse(GenericModel, Generic[T]):
        success: bool
        msg: Optional[str] = None
        data: Optional[T] = None
