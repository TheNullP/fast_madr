FROM archlinux:latest

RUN pacman -Sy --noconfirm \
    python python-pip python-virtualenv poetry \
    postgresql-libs \
    && pacman -Scc --noconfirm #limpa o cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

RUN poetry install --no-root --no-dev

EXPOSE 8000

COPY . .

CMD ["poetry","run", "uvicorn", "fast_madr.main:app", "--host", "0.0.0.0", "--port", "8000"]
