# Code Style Guide

## Python

### Naming

- **Classes**: `PascalCase` (e.g., `HtmlGenerator`, `HassCommunicationsCoordinator`)
- **Methods**: `camelCase` (e.g., `getRequest`, `weather_cell`) — the codebase mixes styles; match the surrounding file
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `HASS_IP`, `PAGE_REFRESH_INTERVAL_SECONDS`)
- **Private attributes**: Prefix with `_` (e.g., `self._h`, `self._hassComms`)

### Docstrings

Use Google-style docstrings on all public methods:

```python
def weather_cell(self):
    """
    Generates an HTML representation of the weather cell.

    Args:
      param_name (type): Description.

    Returns:
      str: Description of return value.
    """
```

- Indent docstring body with 4 spaces (matching PEP 8 standard)
- Include `Args:` section when the method takes parameters beyond `self`
- Always include `Returns:` section

### Indentation

- 4-space indentation (PEP 8 standard). Enforced by ruff.

### Imports

- Standard library first, then local modules
- Use `from module import *` only for `utils.constants`
- Explicit imports everywhere else (e.g., `from Html.htmlGenerator import HtmlGenerator`)

## CSS

- IDs use `snake_case` (e.g., `big_table_cell`, `weather_cell`, `net_stats`)
- Dimensions are fixed to 600x800px for Kobo e-ink screens
- No colors other than black and white
- No JavaScript or interactive elements

## HTML Generation

- Use `HtmlGenerator` methods instead of raw HTML strings
- Pass attributes as a single string (e.g., `"id=weather_cell"`)
- Pass children as a `List[str]`
