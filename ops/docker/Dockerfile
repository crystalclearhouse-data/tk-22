# TK-22 Control Runtime API
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (layer cache)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy runtime source
COPY control/ ./control/

EXPOSE 5000

# Run as non-root user
RUN addgroup --system tk22 && adduser --system --ingroup tk22 tk22
USER tk22

CMD ["python", "control/runtime/api.py"]
