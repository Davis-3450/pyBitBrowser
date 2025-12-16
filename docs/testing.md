# Testing

Unit tests are mock-based and do not require BitBrowser running.

Run from the repo root:

```bash
python -m unittest discover -s test -v
```

Notes:

- Tests live in `test/test_client.py` and mock `requests.Session.post`.
- They validate payload shape (camelCase), typed parsing, and error mapping.

