# Tests, Linter & Makefile Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add pytest test suite, ruff linter (with 4-space migration), and a Makefile with common development commands.

**Architecture:** Add `pyproject.toml` as the single config for ruff and pytest. Tests live in `tests/` mirroring the source structure. Makefile wraps all common commands. Ruff handles both linting and formatting, migrating the codebase from 2-space to 4-space indentation.

**Tech Stack:** pytest, ruff, make, unittest.mock

---

## File Structure

**Create:**
- `pyproject.toml` — ruff + pytest configuration
- `requirements-dev.txt` — dev dependencies (pytest, ruff)
- `Makefile` — development commands
- `tests/__init__.py` — test package marker
- `tests/conftest.py` — shared fixtures (mock HA responses, Flask test client)
- `tests/test_html_generator.py` — HtmlGenerator unit tests
- `tests/test_hass_communications.py` — HassCommunicationsCoordinator unit tests
- `tests/test_html_templates.py` — HtmlTemplates unit tests
- `tests/test_app.py` — Flask route integration tests

**Modify:**
- `Html/htmlGenerator.py` — reformat to 4-space indentation
- `Html/htmlTemplates.py` — reformat to 4-space indentation
- `HomeAssistant/hassCommunicationsCoordinator.py` — reformat to 4-space indentation
- `utils/logger.py` — reformat to 4-space indentation
- `utils/constants.py.customize` — reformat to 4-space indentation
- `app.py` — reformat to 4-space indentation
- `CLAUDE.md` — update commands section and remove "no test suite" note
- `context/styling/formatting.md` — update indentation from 2-space to 4-space

---

### Task 1: Project Configuration (pyproject.toml, requirements-dev.txt, Makefile)

**Files:**
- Create: `pyproject.toml`
- Create: `requirements-dev.txt`
- Create: `Makefile`

- [ ] **Step 1: Create `pyproject.toml`**

```toml
[project]
name = "eink-dashboard"
version = "0.1.0"
requires-python = ">=3.9"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]

[tool.ruff]
target-version = "py39"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I", "W"]
ignore = ["E501"]

[tool.ruff.format]
indent-style = "space"
```

- [ ] **Step 2: Create `requirements-dev.txt`**

```
-r requirements.txt
pytest==8.3.4
ruff==0.9.7
```

- [ ] **Step 3: Create `Makefile`**

```makefile
.PHONY: run test lint format docker-build docker-up docker-down setup

run:
	python app.py

test:
	python -m pytest tests/ -v

lint:
	ruff check .
	ruff format --check .

format:
	ruff check --fix .
	ruff format .

docker-build:
	sudo docker compose build

docker-up:
	sudo docker compose up -d

docker-down:
	sudo docker compose down

setup:
	pip install -r requirements-dev.txt
```

- [ ] **Step 4: Install dev dependencies and verify**

Run: `pip install -r requirements-dev.txt`
Expected: all packages install successfully.

Run: `ruff --version`
Expected: prints ruff version.

Run: `python -m pytest --version`
Expected: prints pytest version.

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml requirements-dev.txt Makefile
git commit -m "feat: add pyproject.toml, dev dependencies, and Makefile"
```

---

### Task 2: Migrate Codebase to 4-Space Indentation with Ruff

**Files:**
- Modify: `app.py`
- Modify: `Html/htmlGenerator.py`
- Modify: `Html/htmlTemplates.py`
- Modify: `HomeAssistant/hassCommunicationsCoordinator.py`
- Modify: `utils/logger.py`
- Modify: `utils/constants.py.customize`
- Modify: `context/styling/formatting.md`

- [ ] **Step 1: Run ruff format on the entire codebase**

Run: `ruff format .`
Expected: all `.py` files reformatted to 4-space indentation. Output lists reformatted files.

- [ ] **Step 2: Run ruff check with auto-fix**

Run: `ruff check --fix .`
Expected: import sorting and minor lint fixes applied.

- [ ] **Step 3: Verify the app still starts**

Run: `python -c "from Html.htmlGenerator import HtmlGenerator; print(HtmlGenerator().p('', ['hello']))"`
Expected: prints `<p >hello</p>` (HTML output, confirming imports work).

- [ ] **Step 4: Update `context/styling/formatting.md`**

Change the indentation section from "2-space indentation" to "4-space indentation (PEP 8 standard). Enforced by ruff."

- [ ] **Step 5: Verify linting passes**

Run: `ruff check . && ruff format --check .`
Expected: no errors, no reformatting needed.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "style: migrate codebase to 4-space indentation via ruff"
```

---

### Task 3: Test Fixtures and HtmlGenerator Tests

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/conftest.py`
- Create: `tests/test_html_generator.py`

- [ ] **Step 1: Create `tests/__init__.py`**

Empty file.

- [ ] **Step 2: Create `tests/conftest.py` with shared fixtures**

```python
import pytest
from unittest.mock import patch, MagicMock

from app import app as flask_app


@pytest.fixture
def client():
    """Flask test client."""
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def mock_hass_response_ok():
    """Factory fixture for successful HA API responses."""
    def _make(state, attributes=None):
        resp = {"state": state, "result": "OK"}
        if attributes:
            resp["attributes"] = attributes
        return resp
    return _make


@pytest.fixture
def mock_hass_response_err():
    """A failed HA API response."""
    return {"result": "err"}
```

- [ ] **Step 3: Write HtmlGenerator tests**

```python
from Html.htmlGenerator import HtmlGenerator


class TestHtmlGenerator:
    def setup_method(self):
        self.h = HtmlGenerator()

    def test_open_close_tag_with_attrs_and_args(self):
        result = self.h.open_close_tag("div", "id=test", ["content"])
        assert "<div id=test>" in result
        assert "content" in result
        assert "</div>" in result

    def test_open_close_tag_empty_args(self):
        result = self.h.open_close_tag("div", "")
        assert "<div >" in result
        assert "</div>" in result

    def test_open_tag(self):
        result = self.h.open_tag("img", ["src='test.png'", "alt='test'"])
        assert "<img src='test.png' alt='test'>" in result

    def test_html_tag_includes_doctype(self):
        result = self.h.html("", ["<head></head>"])
        assert "<!DOCTYPE html>" in result
        assert "<html >" in result
        assert "</html>" in result

    def test_head_tag(self):
        result = self.h.head("", ["<title>Test</title>"])
        assert "<head >" in result
        assert "<title>Test</title>" in result
        assert "</head>" in result

    def test_body_tag(self):
        result = self.h.body("", ["<p>Hello</p>"])
        assert "<body >" in result
        assert "</body>" in result

    def test_table_tag(self):
        result = self.h.table("border=1", ["<tr></tr>"])
        assert "<table border=1>" in result
        assert "</table>" in result

    def test_p_tag(self):
        result = self.h.p("id=test", ["Hello world"])
        assert "<p id=test>" in result
        assert "Hello world" in result

    def test_div_tag(self):
        result = self.h.div("class=box", ["inner"])
        assert "<div class=box>" in result

    def test_img_tag_self_closing(self):
        result = self.h.img(["src='pic.png'", "alt='pic'"])
        assert "<img src='pic.png' alt='pic'>" in result
        assert "</img>" not in result

    def test_link_tag_self_closing(self):
        result = self.h.link(["rel='stylesheet'", "href='style.css'"])
        assert "<link rel='stylesheet' href='style.css'>" in result

    def test_meta_tag_self_closing(self):
        result = self.h.meta(["charset='utf-8'"])
        assert "<meta charset='utf-8'>" in result

    def test_title_tag(self):
        result = self.h.title("", ["My Page"])
        assert "<title >" in result
        assert "My Page" in result
        assert "</title>" in result

    def test_tr_tag(self):
        result = self.h.tr("", ["<td>cell</td>"])
        assert "<tr >" in result
        assert "</tr>" in result

    def test_td_tag(self):
        result = self.h.td("colspan=2", ["data"])
        assert "<td colspan=2>" in result
        assert "data" in result

    def test_br_tag(self):
        result = self.h.br()
        assert "<br" in result

    def test_button_tag(self):
        result = self.h.button("onclick='alert()'", ["Click"])
        assert "<button onclick='alert()'>" in result
        assert "Click" in result

    def test_h1_tag(self):
        result = self.h.h1("id=title", ["Heading"])
        assert "<h1 id=title>" in result
        assert "Heading" in result

    def test_h2_tag(self):
        result = self.h.h2("", ["Sub"])
        assert "<h2 >" in result
        assert "Sub" in result

    def test_nested_tags(self):
        inner = self.h.p("", ["text"])
        result = self.h.div("", [inner])
        assert "<div >" in result
        assert "<p >" in result
        assert "text" in result
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_html_generator.py -v`
Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/
git commit -m "test: add HtmlGenerator unit tests and test fixtures"
```

---

### Task 4: HassCommunicationsCoordinator Tests

**Files:**
- Create: `tests/test_hass_communications.py`

- [ ] **Step 1: Write HassCommunicationsCoordinator tests**

```python
from unittest.mock import patch, MagicMock

from HomeAssistant.hassCommunicationsCoordinator import HassCommunicationsCoordinator


class TestHassCommunicationsCoordinator:
    def setup_method(self):
        with patch("HomeAssistant.hassCommunicationsCoordinator.HASS_IP", "192.168.1.1"), \
             patch("HomeAssistant.hassCommunicationsCoordinator.HASS_PORT", "8123"), \
             patch("HomeAssistant.hassCommunicationsCoordinator.HASS_TOKEN", "test-token"):
            self.coordinator = HassCommunicationsCoordinator()

    @patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
    def test_successful_request(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "state": "sunny",
            "attributes": {"temperature": 22}
        }
        mock_get.return_value = mock_response

        result = self.coordinator.getRequest("sensor.weather")

        assert result["result"] == "OK"
        assert result["state"] == "sunny"
        assert result["attributes"]["temperature"] == 22
        mock_get.assert_called_once()

    @patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
    def test_non_200_status_code(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        result = self.coordinator.getRequest("sensor.weather")

        assert result["result"] == "err"

    @patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
    def test_entity_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Entity not found."}
        mock_get.return_value = mock_response

        result = self.coordinator.getRequest("sensor.nonexistent")

        assert result["result"] == "err"

    @patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
    def test_unavailable_entity(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"state": "unavailable"}
        mock_get.return_value = mock_response

        result = self.coordinator.getRequest("sensor.offline")

        assert result["result"] == "err"

    @patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
    def test_request_includes_auth_header(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"state": "on"}
        mock_get.return_value = mock_response

        self.coordinator.getRequest("sensor.test")

        call_kwargs = mock_get.call_args
        headers = call_kwargs[1]["headers"] if "headers" in call_kwargs[1] else call_kwargs.kwargs["headers"]
        assert "Bearer test-token" in headers["Authorization"]

    @patch("HomeAssistant.hassCommunicationsCoordinator.requests.get")
    def test_request_url_format(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"state": "on"}
        mock_get.return_value = mock_response

        self.coordinator.getRequest("sensor.my_sensor")

        call_args = mock_get.call_args[0][0]
        assert "http://192.168.1.1:8123/api/states/sensor.my_sensor" == call_args
```

- [ ] **Step 2: Run tests to verify they pass**

Run: `python -m pytest tests/test_hass_communications.py -v`
Expected: all tests PASS.

- [ ] **Step 3: Commit**

```bash
git add tests/test_hass_communications.py
git commit -m "test: add HassCommunicationsCoordinator unit tests"
```

---

### Task 5: HtmlTemplates Tests

**Files:**
- Create: `tests/test_html_templates.py`

- [ ] **Step 1: Write HtmlTemplates tests**

```python
from unittest.mock import patch, MagicMock
from Html.htmlTemplates import HtmlTemplates


def _make_ok(state, attributes=None):
    resp = {"state": state, "result": "OK"}
    if attributes:
        resp["attributes"] = attributes
    return resp


ERR_RESPONSE = {"result": "err"}


class TestWeatherConditionFormatter:
    def setup_method(self):
        with patch("Html.htmlTemplates.HASS_IP", "1.1.1.1"), \
             patch("Html.htmlTemplates.HASS_PORT", "8123"), \
             patch("Html.htmlTemplates.HASS_TOKEN", "tok"):
            self.templates = HtmlTemplates()

    def test_known_conditions(self):
        assert self.templates.weather_condition_formatter("sunny") == "Sunny"
        assert self.templates.weather_condition_formatter("cloudy") == "Cloudy"
        assert self.templates.weather_condition_formatter("rainy") == "Rainy"
        assert self.templates.weather_condition_formatter("partlycloudy") == "Partly Cloudy"
        assert self.templates.weather_condition_formatter("clear-night") == "Clear Night"
        assert self.templates.weather_condition_formatter("lightning-rainy") == "Lightning with Rain"

    def test_unknown_condition(self):
        assert self.templates.weather_condition_formatter("unknown") == "Format Err."


class TestWeatherCell:
    def setup_method(self):
        with patch("Html.htmlTemplates.HASS_IP", "1.1.1.1"), \
             patch("Html.htmlTemplates.HASS_PORT", "8123"), \
             patch("Html.htmlTemplates.HASS_TOKEN", "tok"):
            self.templates = HtmlTemplates()

    @patch.object(HtmlTemplates, "_hassComms")
    def test_weather_cell_success(self, mock_comms):
        mock_comms.getRequest.return_value = _make_ok(
            "sunny", {"temperature": 25, "dew_point": 15}
        )
        result = self.templates.weather_cell()
        assert "25" in result
        assert "15" in result
        assert "sunny" in result

    @patch.object(HtmlTemplates, "_hassComms")
    def test_weather_cell_error(self, mock_comms):
        mock_comms.getRequest.return_value = ERR_RESPONSE
        result = self.templates.weather_cell()
        assert "Err" in result


class TestCalendarComponent:
    def setup_method(self):
        with patch("Html.htmlTemplates.HASS_IP", "1.1.1.1"), \
             patch("Html.htmlTemplates.HASS_PORT", "8123"), \
             patch("Html.htmlTemplates.HASS_TOKEN", "tok"):
            self.templates = HtmlTemplates()

    @patch("Html.htmlTemplates.datetime")
    def test_calendar_component(self, mock_datetime):
        mock_now = MagicMock()
        mock_now.strftime.return_value = "Mon Apr 05"
        mock_datetime.datetime.now.return_value = mock_now
        result = self.templates.calendar_component()
        assert "Mon" in result
        assert "Apr" in result
        assert "5" in result


class TestEtaToWork:
    def setup_method(self):
        with patch("Html.htmlTemplates.HASS_IP", "1.1.1.1"), \
             patch("Html.htmlTemplates.HASS_PORT", "8123"), \
             patch("Html.htmlTemplates.HASS_TOKEN", "tok"):
            self.templates = HtmlTemplates()

    @patch.object(HtmlTemplates, "_hassComms")
    def test_eta_success(self, mock_comms):
        mock_comms.getRequest.return_value = _make_ok("23.5")
        result = self.templates.eta_to_work_component()
        assert "23" in result
        assert "Minutes To Work" in result

    @patch.object(HtmlTemplates, "_hassComms")
    def test_eta_error(self, mock_comms):
        mock_comms.getRequest.return_value = ERR_RESPONSE
        result = self.templates.eta_to_work_component()
        assert "Err" in result


class TestPublicIp:
    def setup_method(self):
        with patch("Html.htmlTemplates.HASS_IP", "1.1.1.1"), \
             patch("Html.htmlTemplates.HASS_PORT", "8123"), \
             patch("Html.htmlTemplates.HASS_TOKEN", "tok"):
            self.templates = HtmlTemplates()

    @patch.object(HtmlTemplates, "_hassComms")
    def test_public_ip_success(self, mock_comms):
        mock_comms.getRequest.return_value = _make_ok("203.0.113.1")
        result = self.templates.public_ip()
        assert "203.0.113.1" in result

    @patch.object(HtmlTemplates, "_hassComms")
    def test_public_ip_error(self, mock_comms):
        mock_comms.getRequest.return_value = ERR_RESPONSE
        result = self.templates.public_ip()
        assert "Err" in result


class TestNetStats:
    def setup_method(self):
        with patch("Html.htmlTemplates.HASS_IP", "1.1.1.1"), \
             patch("Html.htmlTemplates.HASS_PORT", "8123"), \
             patch("Html.htmlTemplates.HASS_TOKEN", "tok"):
            self.templates = HtmlTemplates()

    @patch.object(HtmlTemplates, "_hassComms")
    def test_get_net_stat_success(self, mock_comms):
        mock_comms.getRequest.return_value = _make_ok("95.5")
        result = self.templates.get_net_stat("sensor.download")
        assert result == "95.5"

    @patch.object(HtmlTemplates, "_hassComms")
    def test_get_net_stat_error(self, mock_comms):
        mock_comms.getRequest.return_value = ERR_RESPONSE
        result = self.templates.get_net_stat("sensor.download")
        assert result == -1.0

    @patch.object(HtmlTemplates, "_hassComms")
    def test_display_double_net_stat(self, mock_comms):
        mock_comms.getRequest.side_effect = [
            _make_ok("100.5"),
            _make_ok("50.3"),
        ]
        result = self.templates.display_double_net_stat(
            "sensor.lan_dl", "sensor.wan_dl", "Download", "arrow_down"
        )
        assert "100.5" in result
        assert "50.3" in result
        assert "MB/S" in result


class TestGetTime:
    def setup_method(self):
        with patch("Html.htmlTemplates.HASS_IP", "1.1.1.1"), \
             patch("Html.htmlTemplates.HASS_PORT", "8123"), \
             patch("Html.htmlTemplates.HASS_TOKEN", "tok"):
            self.templates = HtmlTemplates()

    @patch("Html.htmlTemplates.datetime")
    def test_current_time(self, mock_datetime):
        mock_now = MagicMock()
        mock_now.strftime.return_value = "14:30"
        mock_datetime.datetime.now.return_value = mock_now
        result = self.templates.get_time(time_type="currentTime")
        assert "14:30" in result

    @patch("Html.htmlTemplates.datetime")
    def test_last_updated(self, mock_datetime):
        mock_now = MagicMock()
        mock_now.strftime.return_value = "14:30"
        mock_datetime.datetime.now.return_value = mock_now
        result = self.templates.get_time(time_type="lastUpdated")
        assert "Last Updated" in result
        assert "14:30" in result

    def test_invalid_time_type(self):
        result = self.templates.get_time(time_type="invalid")
        assert "Invalid time option" in result


class TestPeopleAtHome:
    def setup_method(self):
        with patch("Html.htmlTemplates.HASS_IP", "1.1.1.1"), \
             patch("Html.htmlTemplates.HASS_PORT", "8123"), \
             patch("Html.htmlTemplates.HASS_TOKEN", "tok"):
            self.templates = HtmlTemplates()

    @patch.object(HtmlTemplates, "_hassComms")
    def test_person_home(self, mock_comms):
        mock_comms.getRequest.return_value = _make_ok("home")
        assert self.templates.is_person_home("person.test") is True

    @patch.object(HtmlTemplates, "_hassComms")
    def test_person_away(self, mock_comms):
        mock_comms.getRequest.return_value = _make_ok("not_home")
        assert self.templates.is_person_home("person.test") is False

    @patch.object(HtmlTemplates, "_hassComms")
    def test_person_error(self, mock_comms):
        mock_comms.getRequest.return_value = ERR_RESPONSE
        assert self.templates.is_person_home("person.test") is False
```

- [ ] **Step 2: Run tests to verify they pass**

Run: `python -m pytest tests/test_html_templates.py -v`
Expected: all tests PASS.

- [ ] **Step 3: Commit**

```bash
git add tests/test_html_templates.py
git commit -m "test: add HtmlTemplates unit tests"
```

---

### Task 6: Flask App Route Tests

**Files:**
- Create: `tests/test_app.py`

- [ ] **Step 1: Write Flask route tests**

```python
from unittest.mock import patch


class TestHomeRoute:
    @patch("app.HtmlTemplates")
    def test_home_returns_200(self, mock_templates_cls, client):
        mock_templates_cls.return_value.home.return_value = "<html>dashboard</html>"
        response = client.get("/")
        assert response.status_code == 200
        assert b"dashboard" in response.data

    @patch("app.HtmlTemplates")
    def test_home_calls_html_templates(self, mock_templates_cls, client):
        mock_templates_cls.return_value.home.return_value = "<html></html>"
        client.get("/")
        mock_templates_cls.return_value.home.assert_called_once()


class TestFaviconRoute:
    def test_favicon_returns_200(self, client):
        response = client.get("/favicon.ico")
        assert response.status_code == 200
```

- [ ] **Step 2: Run tests to verify they pass**

Run: `python -m pytest tests/test_app.py -v`
Expected: all tests PASS.

- [ ] **Step 3: Run the full test suite**

Run: `python -m pytest tests/ -v`
Expected: all tests PASS.

- [ ] **Step 4: Commit**

```bash
git add tests/test_app.py
git commit -m "test: add Flask route integration tests"
```

---

### Task 7: Update CLAUDE.md and Styling Docs

**Files:**
- Modify: `CLAUDE.md`
- Modify: `context/styling/formatting.md`

- [ ] **Step 1: Update CLAUDE.md**

In the Commands section, add test and lint commands:

```markdown
### Tests
```bash
make test                        # Run full test suite
python -m pytest tests/ -v       # Equivalent without Make
python -m pytest tests/test_html_generator.py -v          # Single test file
python -m pytest tests/test_html_generator.py::TestHtmlGenerator::test_p_tag -v  # Single test
```

### Linting
```bash
make lint                        # Check linting + formatting
make format                      # Auto-fix lint issues and format
ruff check .                     # Lint only
ruff format .                    # Format only
```
```

Remove the line "No test suite, linter, or CI/CD is configured."

- [ ] **Step 2: Update `context/styling/formatting.md` indentation section**

Change "2-space indentation" to "4-space indentation (PEP 8 standard). Enforced by ruff."

- [ ] **Step 3: Run linting on the full project including tests**

Run: `ruff check . && ruff format --check .`
Expected: no errors, everything formatted.

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md context/styling/formatting.md
git commit -m "docs: update CLAUDE.md with test/lint commands, update style guide to 4-space"
```
