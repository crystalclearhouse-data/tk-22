# TK-22 Deployment Guide

## Overview

TK-22 deploys to Google Cloud Run via GitHub Actions.  Infrastructure is managed
with Terraform (see `ops/terraform/`).  Docker images are stored in Google Artifact
Registry.

---

## Environments

| Environment | Branch / trigger | Cloud Run service |
|-------------|-----------------|-------------------|
| Development | local only | N/A |
| Staging | push to `main` | `tk22-control-api-staging` |
| Production | manual `workflow_dispatch` | `tk22-control-api-production` |

---

## Deploying to Staging (Automatic)

Every merged PR to `main` triggers the `deploy.yml` workflow:

1. Docker image is built and pushed to Artifact Registry.
2. `tk22-control-api-staging` Cloud Run service is updated.
3. Discord notification sent on completion.

---

## Deploying to Production (Manual)

```bash
# Via GitHub UI
1. Go to Actions → Deploy → Run workflow
2. Select environment: production
3. Confirm — only runs from main branch
```

Or via GitHub CLI:

```bash
gh workflow run deploy.yml \
  --ref main \
  -f environment=production
```

---

## Infrastructure Changes (Terraform)

```bash
cd ops/terraform

# 1. Format and validate
terraform fmt -recursive
terraform init
terraform validate

# 2. Plan against an environment
terraform plan -var-file=environments/dev.tfvars

# 3. Apply (requires GCP credentials)
terraform apply -var-file=environments/prod.tfvars
```

Alternatively, use the `terraform.yml` GitHub Actions workflow:

- **PR opened** → plan runs automatically, results posted as PR comment.
- **Manual trigger** → set `apply=true` to apply (runs from `main` only).

---

## Docker Build (Local)

```bash
# Build the control API image
docker build -f ops/docker/Dockerfile -t tk22-control-api:local .

# Run locally with secrets
doppler run -- docker compose -f ops/docker/docker-compose.yml up
```

---

## Rollback

```bash
# Cloud Run — revert to a previous revision
gcloud run services update-traffic tk22-control-api-production \
  --to-revisions=<REVISION_ID>=100 \
  --region us-central1
```

To find available revisions:

```bash
gcloud run revisions list --service tk22-control-api-production --region us-central1
```
