FROM python:3.13-slim-trixie
WORKDIR /app
COPY pyproject.toml uv.lock /app/
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN uv sync --frozen
ENV PATH="/app/.venv/bin:$PATH"
COPY . .
