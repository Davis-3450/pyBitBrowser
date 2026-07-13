# pyBitBrowser

A pythonic API wrapper for BitBrowser's local API

## Usage

```python
from bit_browser.clients import BrowserClient

client = BrowserClient()  # defaults to http://127.0.0.1:54442

# Profiles
profiles = client.list_browsers(page=0, page_size=10)

# Groups (/group/*)
groups = client.group_list_typed(page=0, page_size=10)
```

## Docs

- `docs/README.md`
- `docs/quickstart.md`
- `docs/client.md`
- `docs/models.md`
- `docs/errors.md`
- `docs/testing.md`

## TODO

- [ ] MVP
- Core Features
- [ ] testing scripts (manual)
- [ ] tests (actual unit tests)
- [ ] sync client library

---

Contributors are happily welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for more details <3
