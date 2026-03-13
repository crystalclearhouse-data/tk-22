# TK-22 Infrastructure & Cross-Repository Architecture

## Ecosystem Overview

Crystal Clear Data operates several repositories that together form one end-to-end
product platform.  TK-22 is the **safety verdict engine** at the center of that
platform.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Crystal Clear Data Platform                  │
│                                                                     │
│  tk-22              tk-22-ui           cognitive-ai                 │
│  (verdict engine)   (React/Next.js     (AI reasoning                │
│                      dashboard)         layer)                      │
│       │                   │                   │                     │
│       └───────── POST /execute ───────────────┘                     │
│                          ▼                                          │
│              disco-agent-saas                                       │
│              (agent orchestration)                                  │
│                          │                                          │
│              n8n (automation workflows) ◄── GitHub Actions          │
│                          │                                          │
│          Supabase (database / auth / storage)                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Repository Map

| Repository | Purpose | Primary language | Owned by |
|------------|---------|-----------------|---------|
| `tk-22` | Deterministic safety verdict engine | Python / TypeScript | Backend |
| `tk-22-ui` | User-facing dashboard for TK-22 verdicts | TypeScript / Next.js | Frontend |
| `cognitive-ai` | LLM reasoning and explanation layer | Python | AI |
| `disco-agent-saas` | Agent orchestration and task routing | Python | Backend |

TK-22 is the **only** repository that may produce verdicts.  All other repositories
consume verdict outputs — they never produce them.

---

## TK-22 Internal Layer Model

See `ARCHITECTURE.md` for the full layer contract.  In brief:

```
core/ → adapters/ → services/ → agent/ → apis/ → gen/
 ▲
 └── Only layer that emits a verdict
```

---

## Infrastructure Stack

| Component | Technology | Environment |
|-----------|-----------|-------------|
| Container runtime | Google Cloud Run | Staging + Production |
| Container registry | Google Artifact Registry | Shared |
| Infrastructure as Code | Terraform (`ops/terraform/`) | All |
| Secrets management | Doppler (`doppler.yaml`) | All |
| Local development | Docker Compose (`ops/docker/`) | Dev only |
| Database | Supabase (managed Postgres) | All |
| Automation | n8n (self-hosted or cloud) | All |

---

## Secrets Flow

```
Doppler (source of truth)
       │
       ├─► Local dev:  doppler run -- <cmd>  or  .env  (gitignored)
       │
       ├─► CI (GitHub Actions):  DOPPLER_TOKEN secret → doppler run
       │
       └─► Production (Cloud Run):  GCP Secret Manager
                                    (Terraform provisions the secrets;
                                     values are pushed to Doppler/Secret Manager
                                     by the operator — never stored in code)
```

---

## CI/CD Pipeline

```
developer push / PR
       │
       ├─► build.yml          — lint + typecheck + unit tests (Node + Python)
       │
       ├─► tk22-ci.yml        — full TK-22 system validation
       │
       ├─► tk22-pr-guardian.yml — notifies n8n webhook on PR events
       │
       ├─► terraform.yml      — plan on PR, apply on manual trigger
       │
       └─► deploy.yml         — Docker build + Cloud Run deploy
                                 (staging: automatic on main merge)
                                 (production: manual workflow_dispatch)
```

---

## Environment Promotion

```
Local dev  →  dev (Doppler config)  →  Staging (auto on main merge)  →  Production (manual)
```

Promotion to production requires:

1. All CI checks passing on `main`.
2. Manual `workflow_dispatch` trigger with `environment=production`.
3. Terraform plan reviewed and applied for any infrastructure changes.

---

## Cross-Repository Communication

| From | To | Mechanism |
|------|----|-----------|
| `tk-22-ui` | `tk-22` | HTTP `POST /execute` |
| `disco-agent-saas` | `tk-22` | HTTP `POST /execute` |
| `cognitive-ai` | `tk-22` | verdict read (no write) |
| `tk-22` | Supabase | Python `supabase` client |
| `tk-22` | n8n | Webhook (Discord, ClickUp, etc.) |
| GitHub Actions | n8n | `tk22-pr-guardian.yml` webhook |

---

## Adding a New Service

1. Add required environment variables to `.env.example` and Doppler.
2. Add Terraform resources in `ops/terraform/main.tf` if new GCP infrastructure is needed.
3. Update the Docker Compose file if local dev wiring is required.
4. Update this document.
