# Contribute to pyBitBrowser

Thanks for your interest in improving this library. pyBitBrowser is a lightweight SDK for interacting with the BitBrowser local API. This document explains how to prepare the environment, the style rules, how to propose changes, and what we expect in each PR.

## Principles

- API stable and typed (Pydantic v2), minimal public surface.
- Clear and useful errors (without losing `status_code` or response body).
- Minimal dependencies; avoid new dependencies if not necessary.

## Requirements

- Python 3.10 or higher.
- Access to the BitBrowser local API (for manual tests): default seems to be: `http://127.0.0.1:54442`.
- Operating system: any compatible with Python 3.10+.

## Prepare development environment

- use`uv` (highly recommended) (see [uv docs](https://docs.astral.sh/uv/))
- `uv sync` to install dependencies or `uv sync --dev` to install dev dependencies
- install as a package: `uv pip install -e .`

## Code style

- PEP 8 and type hints
- Pydantic v2 for validation
- snake_case except for models (convenience)

## Commits and branches

- Use Conventional Commits (e.g.: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`).
- Create descriptive branches, e.g.: `feat/async-client`, `fix/error-handling`.

## Tests

- As of now test with your custom script manually.
- Unit tests might be added later.

## Documentation

- Keep `README.md` updated with examples of use (sync/async if applicable).
- [BitBrowser API docs](https://doc.bitbrowser.net/api-docs/local-service-guide-demo-download)

## Checklist for PRs

- [ ] The change is small and focused.
- [ ] Code with type hints and docstrings where it applies.
- [ ] Tests with gists that can be replicated locally. (hopefully, we will move to unit tests later)
- [ ] Errors preserve context (status, message, payload).
- [ ] Documentation updated (README or docstrings).

## Code of conduct

Be respectful, respect the mantainers. Do not use offensive language.

## Security

No include tokens/credentials in issues, PRs or code. Redact/omit sensitive data in examples. (just in case!)

Thanks for contributing!
