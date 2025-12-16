# Errors

Errors are defined in `bit_browser.errors`.

## Exception types

- `BitBrowserError`: base error type for the library.
- `NetworkError`: request couldn’t be sent (connection/timeout, etc).
- `HTTPStatusError`: non-2xx HTTP response from the local API.
- `ResponseDecodeError`: response wasn’t valid JSON.
- `APIError`: BitBrowser returned `success=false` in the JSON envelope.
- `ResponseValidationError`: typed parsing failed (`*_typed` methods).

## Example

```python
from bit_browser.clients import BrowserClient
from bit_browser.errors import APIError, HTTPStatusError

client = BrowserClient()

try:
    client.browser_detail_typed({"id": "bad"})
except APIError as e:
    print("BitBrowser rejected request:", e)
except HTTPStatusError as e:
    print("HTTP error:", e.status_code)
```

