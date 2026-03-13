# Solana Integration

## Overview

TK-22 evaluates Solana SPL tokens for structural safety using on-chain data
fetched through the Helius API. The verdict engine applies deterministic
fail-closed policies — no probabilistic scoring, no fallbacks.

## Data Source

- **Provider**: [Helius](https://helius.dev) — Solana RPC & enriched APIs
- **Adapter**: `src/tk22/adapters/helius/client.ts`
- **Required env**: `HELIUS_API_KEY` (see `.env.example`)

## Chain Facts Collected

| Field                  | Type             | Description                            |
|------------------------|------------------|----------------------------------------|
| `mint`                 | `string`         | SPL token mint address                 |
| `mintAuthorityActive`  | `boolean | null` | Whether mint authority is still active |
| `freezeAuthorityActive`| `boolean | null` | Whether freeze authority is active     |
| `totalSupply`          | `number | null`  | Total token supply                     |
| `topHolderPercent`     | `number | null`  | % held by largest single holder        |
| `topFiveHolderPercent` | `number | null`  | % held by top five holders             |
| `totalHolders`         | `number | null`  | Number of distinct token holders       |
| `recentTxCount`        | `number | null`  | Recent transaction count               |

## Verdict Rules

- Mint authority active or unknown → `FAIL_CLOSED`
- Freeze authority active or unknown → `FAIL_CLOSED`
- Top holder > 50% → `FAIL_CLOSED`
- All checks pass → `SAFE`

See `src/tk22/core/policies.ts` for thresholds and
`src/tk22/core/verdictEngine.ts` for the evaluation logic.

## Status

**Current**: Adapter returns placeholder data (`null` for all fields).
Production Helius API calls are not yet wired.
