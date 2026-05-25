FROM python:3.11-slim

# Instala as dependências de compilação C e PostgreSQL no padrão Debian/Ubuntu
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN pip install --no-cache-dir poetry

WORKDIR /app
COPY . .

RUN poetry install --no-root

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "fast_madr.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
