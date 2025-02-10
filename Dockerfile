# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
WORKDIR /app
COPY deployment/entrypoint.sh ./entrypoint.sh
COPY uv.lock pyproject.toml manage.py .env ./
COPY src ./src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Add a non-root 'app' user to group 'app'.
RUN groupadd app
RUN useradd app -g app

# Transfer ownership of all files to the non-root user.
RUN chmod +x ./entrypoint.sh
RUN chown -R app:app .

# Change user to the app user.
USER app

# Connect to local postgres server
ENV DH_HOST="172.17.0.0/16"

# Reset the entrypoint, don't invoke `uv`
EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
