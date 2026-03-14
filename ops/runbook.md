# TK-22 Operations Runbook

## On-Call Checklist

Before investigating any incident:

- [ ] Check [GitHub Actions](https://github.com/crystalclearhouse-data/tk-22/actions) for recent failed runs
- [ ] Check Cloud Run logs: `gcloud logging read "resource.type=cloud_run_revision" --limit 50`
- [ ] Verify Doppler is reachable: `doppler me`
- [ ] Confirm Supabase is online: check Supabase dashboard

---

## Common Incidents

### API returns 500 / not responding

1. Check Cloud Run revisions for a bad deploy:
   ```bash
   gcloud run revisions list --service tk22-control-api-production --region us-central1
   ```
2. Roll back to last known-good revision (see `deployment.md`).
3. Tail live logs:
   ```bash
   gcloud run services logs tail tk22-control-api-production --region us-central1
   ```

### Secret missing / authentication error

1. Verify the secret exists in Doppler under the correct config (dev/staging/production).
2. Confirm the Cloud Run service account has `secretmanager.secretAccessor` permission.
3. Redeploy the Cloud Run service to pick up any new Secret Manager values.

### CI pipeline failing on main

1. Open the failed workflow run in GitHub Actions.
2. Identify the failing job (lint / test / deploy).
3. If lint: fix locally with `npm run lint` and `npm run typecheck`.
4. If test: run `npm test` locally to reproduce.
5. If deploy: check GCP credentials and Workload Identity Federation setup.

### n8n webhook not receiving events

1. Confirm `N8N_TK22_PR_WEBHOOK` is set correctly in Doppler.
2. Test the webhook manually:
   ```bash
   curl -X POST "$N8N_WEBHOOK_URL" -H "Content-Type: application/json" \
     -d '{"event":"test","repo":"tk-22"}'
   ```
3. Check n8n execution logs for the webhook workflow.

### Helius RPC calls failing

1. Verify `HELIUS_API_KEY` and `HELIUS_RPC_URL` in Doppler.
2. Check [Helius status page](https://status.helius.dev).
3. If quota exceeded, upgrade plan or reduce polling frequency.

---

## Routine Maintenance

| Task | Frequency | Owner |
|------|-----------|-------|
| Rotate API keys (Helius, Stripe, OpenAI) | Quarterly | Backend |
| Review Cloud Run costs | Monthly | Ops |
| Prune old Docker image tags in Artifact Registry | Monthly | Ops |
| Review and merge Dependabot PRs | Weekly | Backend |
| Terraform plan review against production | Before every infra change | Backend |

---

## Contacts

| Role | Contact |
|------|---------|
| Repository owner | @crystalclearhouse-data |
| Automation issues | Check n8n dashboard |
| GCP issues | GCP Cloud Console |
