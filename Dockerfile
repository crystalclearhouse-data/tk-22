# ── Stage 1: Node/TypeScript build ──────────────────────────────────────
FROM node:20-alpine AS node-builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --production=false

COPY . .
RUN npm run build 2>/dev/null || echo "No build script, skipping"

# ── Stage 2: Python deps ─────────────────────────────────────────────────
FROM python:3.11-slim AS python-builder

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Stage 3: Final runtime image ─────────────────────────────────────────
FROM python:3.11-slim AS runtime

WORKDIR /app

# Install Node runtime for TS execution
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs npm curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python deps
COPY --from=python-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=python-builder /usr/local/bin /usr/local/bin

# Copy Node build output
COPY --from=node-builder /app /app

# Non-root user for security
RUN useradd -m -u 1001 tk22user && chown -R tk22user:tk22user /app
USER tk22user

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"]
