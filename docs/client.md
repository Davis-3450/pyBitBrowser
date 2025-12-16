# BrowserClient

`BrowserClient` is the main entry point. It sends `POST` requests to the local API and returns either:

- **raw dict/list** data (`Any`), or
- **typed models** when a `*_typed` method exists.

Import:

```python
from bit_browser.clients import BrowserClient
```

## Browser profiles

Endpoints: `/browser/update`, `/browser/update/partial`, `/browser/open`, `/browser/close`, `/browser/delete`, `/browser/detail`, `/browser/list`, `/users`

- Create/update profile (raw): `browser_update(...)`
- Create/update profile (typed): `browser_update_typed(...)`
- Partial update: `browser_update_partial(...)`
- Open profile (raw): `browser_open(...)`
- Open profile (typed): `browser_open_typed(...)`
- Close profile: `browser_close(...)`
- Delete profile: `browser_delete(...)`
- Profile detail (raw): `browser_detail(...)`
- Profile detail (typed): `browser_detail_typed(...)`
- List profiles (raw): `list_browsers(page, page_size, **filters)`
- List profiles (typed): `list_browsers_typed(page, page_size, **filters)`
- Reset abnormal “opening/closing” state: `users_reset_closed_state(...)`

Notes:

- The API uses camelCase keys (e.g. `proxyMethod`, `browserFingerPrint`). The typed request/response models in this project also use camelCase.
- Some endpoints return variable shapes depending on BitBrowser version; for those, the wrapper exposes raw `Any`.

## Groups

Endpoints: `/group/list`, `/group/add`, `/group/edit`, `/group/delete`, `/group/detail`

- `group_list(...)` / `group_list_typed(...)`
- `group_add(...)` / `group_add_typed(...)`
- `group_edit(...)` / `group_edit_typed(...)`
- `group_delete(...)` / `group_delete_typed(...)`
- `group_detail(...)` / `group_detail_typed(...)`

## Proxy / remark / maintenance

Endpoints: `/browser/proxy/update`, `/browser/remark/update`, `/browser/group/update`, `/browser/close/byseqs`, `/browser/close/all`, `/browser/delete/ids`, `/cache/clear`, `/cache/clear/exceptExtensions`

- Update proxy: `update_proxy(...)` (or `update_proxy_typed(request)` for typed request payload)
- Update remark: `update_remark(browser_ids, remark)`
- Assign profiles to group: `update_group(group_id, browser_ids)`
- Close by seqs: `close_by_seqs(seqs)`
- Close all: `close_all()`
- Delete by ids: `delete_browsers_by_ids(ids)`
- Clear cache: `clear_cache(ids)`
- Clear cache (keep extensions): `clear_cache_except_extensions(ids)`

## Ports / PIDs

Endpoints: `/browser/ports`, `/browser/pids`, `/browser/pids/all`

- `get_opened_ports()`
- `get_pids(ids)`
- `get_all_pids()`

## Window bounds / displays

Endpoints: `/windowbounds`, `/windowbounds/flexable`, `/alldisplays`

- `windowbounds_reset(**window_bounds)`
- `windowbounds_flexible(seqlist=None)`
- `get_all_displays()`

## Cookies

Endpoints: `/browser/cookies/set`, `/browser/cookies/get`, `/browser/cookies/clear`, `/browser/cookies/format`

- `cookies_set(browser_id, cookies)`
- `cookies_get(browser_id)`
- `cookies_clear(browser_id, save_synced=True)`
- `cookies_format(cookie, hostname=None)`

## RPA / utilities

Endpoints: `/rpa/run`, `/rpa/stop`, `/autopaste`, `/utils/readexcel`, `/utils/readfile`

- `rpa_run(task_id)`
- `rpa_stop(task_id)`
- `autopaste(browser_id, url)`
- `utils_read_excel(filepath)`
- `utils_read_file(filepath)`

## Extralog (Local Library Data)

Endpoints: `/extralog/list`, `/extralog/add`, `/extralog/update`, `/extralog/delete`, `/extralog/detail`, `/extralog/clear`

- `extralog_list(...)` / `extralog_list_typed(...)`
- `extralog_add(...)` / `extralog_add_typed(...)`
- `extralog_update(log_id, **fields)`
- `extralog_delete(log_id)`
- `extralog_detail(log_id, **extra)` / `extralog_detail_typed(log_id)`
- `extralog_clear()`

