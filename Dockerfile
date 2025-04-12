# Etapa 1: builder
FROM python:3.13-slim AS builder

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y build-essential curl

# Instala Poetry
RUN pip install poetry

# Copia os arquivos do projeto
COPY . .

# Evita virtualenv e instala dependências somente de produção
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi --no-root

# Etapa 2: runner
FROM python:3.13-slim AS runner

WORKDIR /app

# Copia apenas os arquivos instalados da etapa builder
COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

# Variáveis de ambiente
ENV PORT=8000

EXPOSE ${PORT}

# Comando de inicialização
CMD ["sh", "-c", "gunicorn --workers 1 --bind :$PORT core.wsgi:application"]
