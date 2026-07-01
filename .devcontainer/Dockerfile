FROM python:3.12-slim-bookworm

# System dependencies needed to BUILD some packages from requirements.txt:
#   - default-libmysqlclient-dev + pkg-config + build-essential -> mysqlclient
#   - libjpeg62-turbo-dev, zlib1g-dev                            -> pillow (fallback if no wheel)
#   - libpq-dev                                                  -> psycopg2 fallback (psycopg2-binary usually skips this)
#   - git                                                        -> GitPython needs the actual git binary at runtime
#   - gettext                                                    -> django manage.py compilemessages / makemessages
#   - curl, ca-certificates                                      -> installing uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    git \
    gettext \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv (official static binary image)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

ENV UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/workspace/.venv \
    PATH="/workspace/.venv/bin:$PATH"

WORKDIR /workspace

# Keep the container alive; devcontainer attaches a shell/VS Code to it.
CMD ["sleep", "infinity"]