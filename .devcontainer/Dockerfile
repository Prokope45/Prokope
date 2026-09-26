FROM python:3.13-slim-bookworm

# System dependencies needed to BUILD some packages from requirements.txt:
#   - libjpeg62-turbo-dev, zlib1g-dev                            -> pillow (fallback if no wheel)
#   - libpq-dev                                                  -> psycopg2 fallback (psycopg2-binary usually skips this)
#   - git                                                        -> GitPython needs the actual git binary at runtime
#   - gettext                                                    -> django manage.py compilemessages / makemessages
#   - curl, ca-certificates                                      -> installing uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    git \
    gettext \
    curl \
    ca-certificates \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install PostgreSQL 16 client (matches production server version)
RUN curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc \
    | gpg --dearmor -o /usr/share/keyrings/postgresql-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/postgresql-archive-keyring.gpg] http://apt.postgresql.org/pub/repos/apt bookworm-pgdg main" \
    > /etc/apt/sources.list.d/postgresql.list \
    && apt-get update && apt-get install -y --no-install-recommends postgresql-client-16 \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 LTS and npm for frontend development
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install uv (official static binary image)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

ENV UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/workspace/.venv \
    PATH="/workspace/.venv/bin:$PATH"

WORKDIR /workspace

# Keep the container alive; devcontainer attaches a shell/VS Code to it.
CMD ["sleep", "infinity"]