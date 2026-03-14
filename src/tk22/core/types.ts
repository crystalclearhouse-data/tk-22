export type Verdict = 'SAFE' | 'WARNING' | 'FAIL_CLOSED'

export type ChainFacts = {
  mint: string
  mintAuthorityActive: boolean | null
  freezeAuthorityActive: boolean | null
  totalSupply: number | null
  topHolderPercent: number | null
  topFiveHolderPercent: number | null
  totalHolders: number | null
  recentTxCount: number | null
  fetchedAt: string
  source: 'helius'
}

export type VerdictResult = {
  token: string
  verdict: Verdict
  confidence: number
  signals: Record<string, boolean | number | null>
  reasoning: string[]
  recommendation: 'DO NOT TOUCH' | 'HIGH RISK' | 'STRUCTURALLY SAFE'
}
