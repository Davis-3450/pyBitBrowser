# Models (typed)

Typed models live under `bit_browser.models.*` and use **camelCase attribute names** to match the API.

They are intentionally permissive (`extra="allow"`) because BitBrowser’s local API can add fields across versions.

## Browser models

Module: `bit_browser.models.browser`

- `BrowserUpdateRequest`: payload for `/browser/update`
- `BrowserPartialUpdateRequest`: payload for `/browser/update/partial`
- `BrowserProfile`: profile returned by list/detail/update in most cases
- `BrowserListData`: list response (`totalNum`, `list`)
- `BrowserOpenData`: open response (`ws`, `http`, ...)

## Group models

Module: `bit_browser.models.group`

- `Group`
- `GroupListData`

## Extralog models

Module: `bit_browser.models.extralog`

- `ExtralogItem`
- `ExtralogListData`

## Misc request models

Module: `bit_browser.models.misc`

Request helpers for common endpoints (e.g. `BrowserOpenRequest`, `ProxyUpdateRequest`).

