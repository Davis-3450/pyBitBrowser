"""Errors for bit_browser package."""


class BaseException(Exception):
    pass


class ValidationError(BaseException):
    pass


class BadRequest(BaseException):
    pass
