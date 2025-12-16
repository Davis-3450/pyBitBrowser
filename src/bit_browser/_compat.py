from __future__ import annotations

from typing import Any, Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


def to_camel(string: str) -> str:
    # pydantic v1's `to_camel` uppercases the first letter ("Args"), which is
    # not what BitBrowser expects. Keep the first segment lowercase.
    parts = string.split("_")
    if not parts:
        return string
    return parts[0] + "".join(word[:1].upper() + word[1:] for word in parts[1:] if word)


def model_validate(model: Type[T], obj: Any) -> T:
    mv = getattr(model, "model_validate", None)
    if callable(mv):
        return mv(obj)  # type: ignore[misc]
    # Pydantic v1
    return model.parse_obj(obj)  # type: ignore[attr-defined]


def model_dump(
    instance: BaseModel, *, by_alias: bool = True, exclude_none: bool = True
) -> dict[str, Any]:
    md = getattr(instance, "model_dump", None)
    if callable(md):
        return md(by_alias=by_alias, exclude_none=exclude_none)  # type: ignore[misc]
    return instance.dict(by_alias=by_alias, exclude_none=exclude_none)  # type: ignore[call-arg]
