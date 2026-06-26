FROM python:3.9-slim

# uv binary, used to install the locked dependencies
COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /uvx /bin/

WORKDIR /app

# Install runtime dependencies from the lockfile first, for layer caching.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . /app
EXPOSE 6123
CMD [".venv/bin/gunicorn", "-w", "4", "-b", "0.0.0.0:6123", "-t", "0", "app:app"]
