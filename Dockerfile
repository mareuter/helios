FROM python:3.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN  apt update && \
     apt-get install --yes git

COPY . .

RUN pip wheel --wheel-dir wheels -e .

FROM python:3.12-slim

LABEL maintainer="Michael Reuter"
LABEL org.opencontainers.image.source=https://github.com/mareuter/helios
LABEL org.opencontainers.image.description="Webservice for sun information."
LABEL org.opencontainers.image.license=BSD-3-Clause

RUN adduser fastapi
USER fastapi
WORKDIR /home/fastapi

ENV PATH="/home/fastapi/.local/bin:${PATH}"

RUN --mount=type=bind,from=builder,source=/app/wheels,target=wheels \
    pip install --no-cache-dir --user wheels/*

EXPOSE 8000

CMD ["uvicorn", "helios.main:app", "--host", "0.0.0.0"]
