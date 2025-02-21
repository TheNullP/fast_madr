FROM archlinux:latest

RUN pacman-key --init && pacman-key --populate archlinux

RUN pacman -Sy --noconfirm \
    python python-pip python-virtualenv poetry \
    postgresql-libs \
    && pacman -Scc --noconfirm #limpa o cache


WORKDIR /app
COPY . .

RUN poetry install --no-root 


EXPOSE 8000

 CMD ["poetry", "run", "uvicorn", "fast_madr.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
