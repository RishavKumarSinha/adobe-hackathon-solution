FROM --platform=linux/amd64 python:3.10 as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

COPY models/minilm /app/models/minilm

COPY challenge_1a /app/challenge_1a
COPY challenge_1b /app/challenge_1b
COPY main.py .

ENTRYPOINT ["python", "main.py"]