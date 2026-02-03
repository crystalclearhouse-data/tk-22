#!/usr/bin/env bash
set -euo pipefail

PLAN="docs/MULTI_REPO_BOUNDARY_PLAN.md"
OUT="reports/repo-split-dry-run.md"

mkdir -p reports

echo "# Repo Split — Phase 1 Dry Run" > "$OUT"
echo "" >> "$OUT"
date -u +"Generated: %Y-%m-%dT%H:%M:%SZ" >> "$OUT"
echo "" >> "$OUT"

if [[ ! -f "$PLAN" ]]; then
  echo "❌ Missing plan: $PLAN"
  exit 1
fi

echo "## Inputs" >> "$OUT"
echo "- Plan: $PLAN" >> "$OUT"
echo "" >> "$OUT"

echo "## Detected Top-Level Folders" >> "$OUT"
ls -1 | sed 's/^/- /' >> "$OUT"
echo "" >> "$OUT"

echo "## Proposed Ownership (Simulation)" >> "$OUT"
cat <<'EOF' >> "$OUT"
- crystalclearhouse / tk-22:
  - agents/
  - automation/
  - rules/
  - infra/
- thediscobass:
  - public-site/
  - chat-widget/
  - brand-content/
- the-steele-zone:
  - experiments/
  - consulting/
  - personal-workflows/
EOF

echo "" >> "$OUT"
echo "## Safety Checks" >> "$OUT"
echo "- No files moved: ✅" >> "$OUT"
echo "- No Git changes: ✅" >> "$OUT"
echo "- No remotes touched: ✅" >> "$OUT"
echo "" >> "$OUT"

echo "## Next Approval Gates" >> "$OUT"
cat <<'EOF' >> "$OUT"
- [ ] Approve ownership map
- [ ] Create empty target repos
- [ ] Copy (not move) files
- [ ] Verify control plane integrity
EOF

echo "✅ Dry-run report written to $OUT"
