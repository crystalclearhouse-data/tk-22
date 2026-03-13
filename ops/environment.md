# TK-22 Environment & Secrets Management

## Strategy

TK-22 uses **Doppler** as the single source of truth for all secrets and environment
variables.  No secrets ever live in committed code, CI logs, or plaintext config files.

### Why Doppler

| Need | Doppler feature |
|------|----------------|
| One place for all secrets | Centralized project dashboard |
| Per-environment overrides | `dev` / `staging` / `production` configs |
| CI/CD injection | `DOPPLER_TOKEN` secret in GitHub Actions |
| Local dev bootstrap | `doppler run --` or `doppler secrets download` |
| Audit log | Every access/change is logged with actor |

---

## Project / Config structure

```
Doppler project: tk-22
├── dev           ← used locally and in CI on pull requests
├── staging       ← used when deploying to staging Cloud Run
└── production    ← used when deploying to production Cloud Run
```

---

## Local Development Setup

```bash
# 1. Install Doppler CLI
brew install dopplerhq/cli/doppler   # macOS
# or: https://docs.doppler.com/docs/install-cli

# 2. Authenticate
doppler login

# 3. Link this repo to the tk-22 project
doppler setup         # follow prompts, choose project=tk-22 config=dev

# 4. Run the API with secrets injected
doppler run -- python control/runtime/api.py

# 5. Or bootstrap a local .env (gitignored)
doppler secrets download --no-file --format env > .env
```

---

## CI/CD Secret Injection

In GitHub Actions, secrets are injected using a repository-level `DOPPLER_TOKEN`
(set in *Settings → Secrets → Actions*).  Workflows use the token like this:

```yaml
- name: Fetch secrets from Doppler
  uses: dopplerhq/cli-action@v3
  with:
    doppler-token: ${{ secrets.DOPPLER_TOKEN }}
    inject-env-vars: true
```

For GCP deployments the following additional secrets must be set as GitHub Actions
secrets (not via Doppler, because they are used to authenticate to GCP before
Doppler can be reached):

| Secret name | Purpose |
|-------------|---------|
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | Workload Identity Federation provider |
| `GCP_SERVICE_ACCOUNT` | Deployer service account email |
| `GCP_PROJECT_ID` | GCP project ID |
| `GCP_REGION` | Default deployment region |

---

## Required Variables

See `.env.example` in the repository root for the full list.  Each key must have
a corresponding entry in the Doppler `dev`, `staging`, and `production` configs.

---

## Secret Rotation

1. Update the value in Doppler for the affected config(s).
2. For Cloud Run workloads, redeploy the service (new revision picks up the secret).
3. For n8n or external services, update their credentials manually.
4. Log the rotation in the relevant ClickUp task.
