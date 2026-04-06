# Home Assistant Offline Landing Page

## Problem

When Home Assistant is unreachable (network down, HA stopped, etc.), the dashboard crashes with an unhandled `ConnectionError` from `requests.get`. The user sees a Flask error page instead of something useful.

## Goal

Display a simple "Home Assistant is offline" page when HA cannot be reached. Since the page auto-refreshes every 60 seconds via meta-refresh, it will automatically recover once HA comes back online.

## Design

### Approach: Upfront health check in `HassCommunicationsCoordinator`

A new `isReachable()` method on the coordinator tests HA connectivity before the dashboard is built. `HtmlTemplates.home()` branches on this result — offline page or normal dashboard.

### `HassCommunicationsCoordinator` changes

**New method — `isReachable()`:**
- Sends a GET request to the HA API root (`/api/`), which returns `{"message": "API running."}` on a healthy instance.
- Wraps the call in try/except for `requests.ConnectionError`, `requests.Timeout`, and `requests.RequestException`.
- Uses a short timeout (5 seconds) to avoid hanging the page.
- Returns `True` if status code is 200, `False` otherwise.

**Existing method — `getRequest()`:**
- Wrap the existing `requests.get` call in a try/except for `requests.RequestException`.
- On exception, log the error and return `{"result": "err"}` (same shape as existing error returns).
- This prevents crashes if HA goes down between the health check and individual sensor requests (race condition).

### `HtmlTemplates` changes

**New method — `offline_page()`:**
- Builds a full HTML page using existing `HtmlGenerator` methods.
- Same `<head>` as the normal dashboard: CSS stylesheet link, viewport meta, meta-refresh at `PAGE_REFRESH_INTERVAL_SECONDS`.
- `<body>` contains a centered "Home Assistant is offline" as a large heading, with the current time displayed below it.
- Uses `HtmlGenerator` tag methods — no raw HTML strings.

**Modified method — `home()`:**
- At the top, calls `self._hassComms.isReachable()`.
- If `False`, returns `self.offline_page()`.
- If `True`, proceeds with the existing dashboard build logic.

### CSS

- New `#offline_message` style for the centered large text. Only basic properties: `text-align: center`, `font-size`, `margin`. No modern CSS features.
- The time reuses the existing `#h1_time` style.
- The offline page styles must not use fixed pixel dimensions for positioning — use percentage-based or relative values so the page renders correctly on devices of different screen sizes, not just 600x800.

### No changes to `app.py`

The Flask route stays as-is — `HtmlTemplates().home()` internally decides which page to return.

### Page content when offline

```
          Home Assistant is offline

                  HH:MM
```

Centered on screen regardless of device dimensions. Large bold text for readability. Auto-refreshes every `PAGE_REFRESH_INTERVAL_SECONDS`.

---

# Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Display an auto-refreshing "Home Assistant is offline" page when HA is unreachable, instead of crashing.

**Architecture:** Upfront health check via `HassCommunicationsCoordinator.isReachable()` before building the dashboard. `HtmlTemplates.home()` branches on the result — offline page or normal dashboard. Existing `getRequest()` also gets exception handling for race conditions.

**Tech Stack:** Python, Flask, requests, pytest, unittest.mock

---

## File Map

- **Modify:** `HomeAssistant/hassCommunicationsCoordinator.py` — add `isReachable()`, add try/except to `getRequest()`
- **Modify:** `Html/htmlTemplates.py` — add `offline_page()`, modify `home()` to branch
- **Modify:** `static/css/styles.css` — add `#offline_message` style
- **Modify:** `tests/test_hass_communications.py` — tests for `isReachable()` and `getRequest()` exception handling
- **Modify:** `tests/test_html_templates.py` — tests for `offline_page()` and `home()` branching

---

### Task 1: Add `isReachable()` to `HassCommunicationsCoordinator`

**Files:**
- Modify: `HomeAssistant/hassCommunicationsCoordinator.py`
- Modify: `tests/test_hass_communications.py`

- [x] **Step 1: Write failing tests for `isReachable()`**

Add to `tests/test_hass_communications.py`:

```python
@patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
def test_is_reachable_returns_true_when_api_healthy(self, mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    assert self.coordinator.isReachable() is True
    mock_get.assert_called_once_with(
        "http://192.168.1.1:8123/api/",
        headers=self.coordinator._headers,
        timeout=5,
    )

@patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
def test_is_reachable_returns_false_on_non_200(self, mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 503
    mock_get.return_value = mock_response

    assert self.coordinator.isReachable() is False

@patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
def test_is_reachable_returns_false_on_connection_error(self, mock_get):
    mock_get.side_effect = requests.ConnectionError()

    assert self.coordinator.isReachable() is False

@patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
def test_is_reachable_returns_false_on_timeout(self, mock_get):
    mock_get.side_effect = requests.Timeout()

    assert self.coordinator.isReachable() is False
```

Also add `import requests` at the top of the test file (needed for `requests.ConnectionError` and `requests.Timeout`).

- [x] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_hass_communications.py -v -k "is_reachable"`
Expected: FAIL — `AttributeError: 'HassCommunicationsCoordinator' object has no attribute 'isReachable'`

- [x] **Step 3: Implement `isReachable()`**

Add to `HomeAssistant/hassCommunicationsCoordinator.py`, after `__init__`:

```python
def isReachable(self):
    """
    Checks if the Home Assistant API is reachable.

    Sends a GET request to the API root with a 5-second timeout.

    Returns:
      bool: True if the API responds with status 200, False otherwise.
    """
    try:
        response = requests.get(
            self._address,
            headers=self._headers,
            timeout=5,
        )
        return response.status_code == 200
    except requests.RequestException:
        return False
```

- [x] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_hass_communications.py -v -k "is_reachable"`
Expected: 4 PASSED

- [x] **Step 5: Run full test suite to check for regressions**

Run: `python3 -m pytest tests/ -v`
Expected: All tests PASS

---

### Task 2: Add exception handling to `getRequest()`

**Files:**
- Modify: `HomeAssistant/hassCommunicationsCoordinator.py`
- Modify: `tests/test_hass_communications.py`

- [x] **Step 1: Write failing test for `getRequest()` exception handling**

Add to `TestHassCommunicationsCoordinator` in `tests/test_hass_communications.py`:

```python
@patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
def test_get_request_returns_err_on_connection_error(self, mock_get):
    mock_get.side_effect = requests.ConnectionError()

    result = self.coordinator.getRequest("sensor.weather")

    assert result["result"] == "err"
```

- [x] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_hass_communications.py::TestHassCommunicationsCoordinator::test_get_request_returns_err_on_connection_error -v`
Expected: FAIL — `ConnectionError` raised (unhandled)

- [x] **Step 3: Wrap `getRequest()` in try/except**

In `HomeAssistant/hassCommunicationsCoordinator.py`, modify `getRequest()` to wrap the entire body in a try/except:

```python
def getRequest(self, id):
    """
    Fetches the state of a Home Assistant entity by ID.

    Args:
      id (str): The entity ID to fetch.

    Returns:
      dict: The entity state as a dict with a "result" key set to "OK" on success
          or "err" on failure.
    """
    try:
        response = requests.get(f"{self._address}states/{id}", headers=self._headers)
    except requests.RequestException:
        logger.error(f"Connection failed for {id}")
        return {"result": "err"}

    response_json = response.json()

    if response.status_code != 200:
        logger.error(f"Error getting state for {id}: {response.status_code}")
        return {"result": "err"}

    if "message" in response_json and response_json["message"] == "Entity not found.":
        logger.error(f"This entity does not exist: {id}")
        return {"result": "err"}

    if "state" in response_json and response_json["state"] == "unavailable":
        logger.error(f"Unavailable entity w/ id: {id}")
        return {"result": "err"}

    response_json["result"] = "OK"
    return response_json
```

- [x] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_hass_communications.py -v`
Expected: All tests PASS (including the new one)

---

### Task 3: Add CSS for offline page

**Files:**
- Modify: `static/css/styles.css`

- [x] **Step 1: Add `#offline_message` style**

Append to `static/css/styles.css`:

```css
#offline_message {
  text-align: center;
  font-size: 40px;
  font-weight: bold;
  margin-top: 30%;
}
```

This uses `margin-top: 30%` (percentage-based) to roughly center vertically on any screen size.

- [x] **Step 2: Run linter**

Run: `make lint`
Expected: PASS (no CSS linting issues)

---

### Task 4: Add `offline_page()` to `HtmlTemplates`

**Files:**
- Modify: `Html/htmlTemplates.py`
- Modify: `tests/test_html_templates.py`

- [x] **Step 1: Write failing tests for `offline_page()`**

Add to `tests/test_html_templates.py`:

```python
class TestOfflinePage:
    def setup_method(self):
        self.templates = _make_templates()

    def test_offline_page_contains_offline_message(self):
        result = self.templates.offline_page()
        assert "Home Assistant is offline" in result

    @patch("Html.htmlTemplates.datetime")
    def test_offline_page_contains_current_time(self, mock_datetime):
        mock_now = MagicMock()
        mock_now.strftime.return_value = "14:30"
        mock_datetime.datetime.now.return_value = mock_now
        result = self.templates.offline_page()
        assert "14:30" in result

    def test_offline_page_contains_meta_refresh(self):
        result = self.templates.offline_page()
        assert "http-equiv='refresh'" in result

    def test_offline_page_contains_stylesheet(self):
        result = self.templates.offline_page()
        assert "stylesheet" in result

    def test_offline_page_has_offline_message_id(self):
        result = self.templates.offline_page()
        assert "offline_message" in result
```

- [x] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_html_templates.py::TestOfflinePage -v`
Expected: FAIL — `AttributeError: 'HtmlTemplates' object has no attribute 'offline_page'`

- [x] **Step 3: Implement `offline_page()`**

Add to `Html/htmlTemplates.py`, after the `home()` method:

```python
def offline_page(self):
    """
    Generates an HTML page indicating Home Assistant is offline.

    Displays a centered "Home Assistant is offline" message with the
    current time below it. Includes meta-refresh so the page will
    automatically recover when Home Assistant comes back online.

    Returns:
      str: The HTML content for the offline page.
    """
    return self._h.html(
        "",
        [
            self._h.head(
                "",
                [
                    self._h.link([f"rel='stylesheet' type='text/css' href={CSS_STYLESHEET_PATH}"]),
                    self._h.meta(["name='viewport' content='width=device-width' initial-scale=1.0"]),
                    self._h.meta([f"http-equiv='refresh' content={PAGE_REFRESH_INTERVAL_SECONDS}"]),
                    self._h.title("", ["Dashboard"]),
                ],
            ),
            self._h.body(
                "",
                [
                    self._h.div(
                        "id=offline_message",
                        [
                            self._h.h1("", ["Home Assistant is offline"]),
                            self._h.p("", [f"{datetime.datetime.now().strftime('%H:%M')}"]),
                        ],
                    ),
                ],
            ),
        ],
    )
```

- [x] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_html_templates.py::TestOfflinePage -v`
Expected: 5 PASSED

---

### Task 5: Modify `home()` to branch on `isReachable()`

**Files:**
- Modify: `Html/htmlTemplates.py`
- Modify: `tests/test_html_templates.py`

- [x] **Step 1: Write failing tests for `home()` branching**

Add to `tests/test_html_templates.py`:

```python
class TestHomeBranching:
    def setup_method(self):
        self.templates = _make_templates()
        self.mock_comms = self.templates._hassComms

    def test_home_returns_offline_page_when_unreachable(self):
        self.mock_comms.isReachable.return_value = False
        result = self.templates.home()
        assert "Home Assistant is offline" in result

    def test_home_returns_dashboard_when_reachable(self):
        self.mock_comms.isReachable.return_value = True
        self.mock_comms.getRequest.return_value = _make_ok("sunny", {"temperature": 25, "dew_point": 15})
        result = self.templates.home()
        assert "Home Assistant is offline" not in result
        assert "table" in result
```

- [x] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_html_templates.py::TestHomeBranching -v`
Expected: FAIL — `home()` does not call `isReachable()` yet

- [x] **Step 3: Add `isReachable()` check to `home()`**

In `Html/htmlTemplates.py`, add at the top of the `home()` method body, before the existing `return` statement:

```python
if not self._hassComms.isReachable():
    return self.offline_page()
```

- [x] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_html_templates.py::TestHomeBranching -v`
Expected: 2 PASSED

- [x] **Step 5: Run full test suite and linter**

Run: `make test && make lint`
Expected: All tests PASS, no lint errors
