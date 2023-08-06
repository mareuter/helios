FROM python:3.11-slim

LABEL maintainer="Michael Reuter"
LABEL org.opencontainers.image.source=https://github.com/mareuter/helios
LABEL org.opencontainers.image.description="Webservice for sun information."
LABEL org.opencontainers.image.license=BSD-3-Clause

WORKDIR /
RUN pip install --upgrade pip

RUN adduser fastapi
USER fastapi
WORKDIR /home/fastapi

COPY --chown=fastapi:fastapi requirements requirements
COPY --chown=fastapi:fastapi requirements.txt .
COPY --chown=fastapi:fastapi bin bin
COPY --chown=fastapi:fastapi app app

ENV PATH="/home/fastapi/.local/bin:${PATH}"

RUN pip install --user -r requirements.txt && \
    python bin/setup_skyfield.py

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
