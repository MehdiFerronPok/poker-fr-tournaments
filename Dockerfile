FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# D�pendances syst�me minimales (psycopg2, geo libs si besoin)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installer Poetry sans venv
RUN pip install --no-cache-dir pipx && pipx install poetry && pipx ensurepath
ENV PATH=/root/.local/bin:$PATH

COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root

# Copier le code
COPY . .

# Port par d�faut en local, mais Fly d�finit $PORT � l'ex�cution
ENV PORT=8080

# Lancer l'API
CMD ["sh","-c","uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
