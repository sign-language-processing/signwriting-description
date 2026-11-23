FROM python:3.15.2-slim-trixie AS builder
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml README.md ./
COPY signwriting_description/ ./signwriting_description/
RUN python -m venv --without-pip /opt/venv \
    && python -m pip --python /opt/venv/bin/python install --no-cache-dir ".[server]"

FROM python:3.15.2-slim-trixie AS runtime
RUN apt-get update && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* /usr/local/lib/python3.15/ensurepip /usr/local/lib/python3.15/site-packages /usr/local/bin/pip*
RUN useradd --create-home --uid 1000 app
WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH" PYTHONUNBUFFERED=1 PORT=8080
COPY --from=builder /opt/venv /opt/venv
COPY signwriting_description/ ./signwriting_description/
USER app
EXPOSE 8080
CMD exec uvicorn signwriting_description.server:app --host 0.0.0.0 --port $PORT --workers 1
