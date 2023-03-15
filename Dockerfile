FROM python:3.10-slim

LABEL maintainer="Michael Reuter"

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

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
