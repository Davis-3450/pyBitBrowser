"""Error hierarchy for the BitBrowser client."""


class BitBrowserError(Exception):
    """Base error for this library."""


class APIError(BitBrowserError):
    """BitBrowser returned `success=false`."""

    def __init__(self, message: str | None = None, *, data=None):
        super().__init__(message or "API error")
        self.data = data


class HTTPStatusError(BitBrowserError):
    """Non-2xx HTTP response."""

    def __init__(self, status_code: int, body: str | None = None):
        super().__init__(f"HTTP {status_code}: {body or ''}".strip())
        self.status_code = status_code
        self.body = body


class NetworkError(BitBrowserError):
    """requests-level error (connection/timeout/etc)."""


class ResponseDecodeError(BitBrowserError):
    """Response body wasn't valid JSON."""


class ResponseValidationError(BitBrowserError):
    """Response JSON didn't match the expected schema."""

