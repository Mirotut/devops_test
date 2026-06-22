FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /worker

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# gosu lets the entrypoint fix bind-mount ownership then drop to non-root
RUN apt-get update -qq && apt-get install -y --no-install-recommends gosu && \
    rm -rf /var/lib/apt/lists/*

RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup --no-create-home appuser

RUN mkdir -p /var/log/worker

COPY worker.py docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

EXPOSE 5001

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5001/health')" || exit 1

# Container starts as root so entrypoint can chown the mounted log dir,
# then gosu drops privileges to appuser before exec-ing the app.
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python", "worker.py"]
