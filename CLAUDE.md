# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python Flask web server that renders a Home Assistant dashboard optimized for e-ink displays (Kobo e-readers). The server fetches sensor data from Home Assistant's REST API and generates a static HTML page with auto-refresh. No JavaScript — pure server-side HTML generation with CSS styling tuned for 600x800px e-ink screens rotated 180° for landscape orientation.

## Commands

### Local Development
```bash
make run                         # Flask debug server on 0.0.0.0:6123
make setup                       # Install all dependencies (including dev)
```

### Tests
```bash
make test                        # Run full test suite
python3 -m pytest tests/ -v      # Equivalent without Make
python3 -m pytest tests/test_html_generator.py -v          # Single test file
python3 -m pytest tests/test_html_generator.py::TestHtmlGenerator::test_p_tag -v  # Single test
```

### Linting
```bash
make lint                        # Check linting + formatting
make format                      # Auto-fix lint issues and format
ruff check .                     # Lint only
ruff format .                    # Format only
```

### Docker Deployment
```bash
make docker-up                   # Build and run (recommended)
make docker-build                # Build only
make docker-down                 # Stop containers
```

## Setup

Copy `utils/constants.py.customize` to `utils/constants.py` and fill in Home Assistant connection details and sensor IDs. This file is gitignored.

## Architecture

**Request flow:** Browser → Flask (`app.py`) → `HtmlTemplates.home()` → `HassCommunicationsCoordinator.getRequest()` per sensor → Home Assistant REST API → HTML response with meta-refresh.

### Key Files

- **`app.py`** — Flask entry point. Two routes: `/` (dashboard) and `/favicon.ico`.
- **`Html/htmlTemplates.py`** — Core logic. `HtmlTemplates` class builds the full dashboard page by fetching each sensor and composing HTML via `HtmlGenerator`. Each dashboard cell (weather, calendar, presence, network stats) is a separate method.
- **`Html/htmlGenerator.py`** — HTML tag builder utility. Generates tags with attributes; used by `htmlTemplates.py` instead of a template engine.
- **`HomeAssistant/hassCommunicationsCoordinator.py`** — API client. `getRequest(id)` fetches entity state from Home Assistant using Bearer token auth.
- **`utils/constants.py`** — All configuration: HA connection, sensor IDs, refresh interval. Created from `.customize` template.
- **`static/css/styles.css`** — eInk-optimized CSS. 180° rotation, large fonts, black-on-white, fixed 600x800px dimensions.
- **`static/assets/weather_svg/`** — SVG icons for weather conditions.

### Design Constraints

This project targets very old e-readers and legacy devices that do not support modern HTML or CSS. Every line of generated HTML and CSS must be kept as simple and backward-compatible as possible — avoid modern CSS features (flexbox, grid, CSS variables, `calc()`, etc.), HTML5 semantic elements, and anything that requires recent browser engine support.

- Table-based HTML layout for compatibility with older e-reader browsers
- No JavaScript — auto-refresh via `<meta http-equiv="refresh">`
- All styling is black-on-white for e-ink contrast
- Production uses Gunicorn with 4 workers (see `dockerfile`)
- Docker Compose mounts source directories as volumes for live editing

## Key References

- **Code style:** [`context/styling/formatting.md`](context/styling/formatting.md) — naming, formatting, docstrings
- **Design specs & plans:** [`context/planning/`](context/planning/) — read before making architectural changes

## Planning Workflow

All plans live under `context/planning/`. **This overrides any skill default** (e.g., `docs/superpowers/plans/` or `docs/superpowers/specs/`) — always save plans, specs, and design docs to `context/planning/`. The design plan and implementation plan for a given task **must** be in the same file — design first, implementation checklist appended below after approval.

When the user asks to plan a task, write the plan as a `.md` file inside `context/planning/` before doing any implementation work. File names must be descriptive kebab-case (e.g., `add-calendar-integration.md`). After writing the plan, notify the user of the file path and wait for explicit approval before proceeding. The user may edit the plan file directly using `/user <comment>` annotations; when new additions to the plan are made in response to comments mark them with `/new`; delete all the `/new` already present in a plan when updating or adding the todo list; implementation begins only after the user explicitly approves. Plans are committed to git alongside code and are never deleted.

**Important**: When writing a plan, include ONLY the architectural design and approach — no implementation checklists or checkboxes. The user will ask for implementation steps separately after approving the plan. Do not add execution details, step numbering, or checkbox lists unless the user explicitly requests them.

Once a plan is approved and the user asks for implementation steps, create an implementation checklist in the plan file. After implementation begins, follow the checklist in order, checking each box (`- [x]`) immediately upon completing the corresponding task.

When implementing new methods always add docstrings in accordance with the directives in `context/styling/formatting.md`.

**Asking Questions**: ALWAYS ask any clarifying questions you need and avoid assumptions unless asked otherwise.

## Prefer Make Commands

Always use `make` targets (e.g., `make test`, `make lint`, `make format`) instead of running the underlying commands directly when a matching Make target exists. Check the Makefile before running raw commands.

## Test-Driven Development

Always write tests before implementation code. Write a failing test first, then write the minimal code to make it pass, then refactor. Use the `superpowers:test-driven-development` skill when implementing features or bugfixes.

## No Auto-Commits

Never run `git commit`, `git push`, or any git write operations unless the user explicitly asks. Stage and commit decisions are always the user's to make.

## Superpowers Skills

Use these skills proactively when the situation calls for them:

- **`superpowers:brainstorming`** — before any creative work: creating features, building components, adding functionality, or modifying behavior
- **`superpowers:writing-plans`** — when you have a spec or requirements for a multi-step task, before touching code
- **`superpowers:executing-plans`** — when executing a written implementation plan
- **`superpowers:test-driven-development`** — when implementing any feature or bugfix
- **`superpowers:systematic-debugging`** — when encountering any bug, test failure, or unexpected behavior
- **`superpowers:verification-before-completion`** — before claiming work is complete or creating PRs
- **`superpowers:requesting-code-review`** — when completing tasks or implementing major features
- **`superpowers:finishing-a-development-branch`** — when implementation is complete and ready to integrate
