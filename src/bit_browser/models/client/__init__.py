from pydantic import BaseModel


class APIResponse(BaseModel):
    success: bool
    msg: str | None = None
    data: dict | list | None = None
