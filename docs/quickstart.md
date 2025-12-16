# Quickstart

## Requirements

- Python `>=3.10`
- BitBrowser installed and its **local API service running**
- Default base URL is `http://127.0.0.1:54442` (see `src/bit_browser/constants/__init__.py`)

## Install (editable)

From the repo root:

```bash
pip install -e .
```

## Basic usage

```python
from bit_browser.clients import BrowserClient

client = BrowserClient()  # defaults to http://127.0.0.1:54442

# List profiles (raw dict response)
profiles = client.list_browsers(page=0, page_size=10)

# List profiles (typed)
profiles_typed = client.list_browsers_typed(page=0, page_size=10)
print(profiles_typed.totalNum)

# Open a profile (typed)
open_info = client.browser_open_typed({"id": "PROFILE_ID"})
print(open_info.ws, open_info.http)
```

## Changing host/port

```python
from bit_browser.clients import BrowserClient

client = BrowserClient(url="http://127.0.0.1:12345")
```

## Auth token (optional)

If your BitBrowser local API is configured with an API key:

```python
client = BrowserClient(token="YOUR_TOKEN")
```

