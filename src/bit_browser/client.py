from __future__ import annotations

from typing import Optional

from bit_browser.clients.browser import BrowserClient

_client: Optional[BrowserClient] = None


def get_client(token: Optional[str] = None) -> BrowserClient:
    """Return a lazily-instantiated, shared :class:`BrowserClient`.

    The client is created on first call. Pass ``token`` on the first call to
    authenticate; subsequent calls return the same instance regardless of the
    argument. Use :func:`reset_client` to force a new instance.
    """
    global _client
    if _client is None:
        _client = BrowserClient(token=token)
    return _client


def reset_client() -> None:
    """Discard the cached client so the next :func:`get_client` rebuilds it."""
    global _client
    _client = None
