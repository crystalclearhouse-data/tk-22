import { ChainFacts } from '../../core/types'

export async function fetchChainFacts(mint: string): Promise<ChainFacts> {
  // Placeholder — execution happens locally or in CI later
  return {
    mint,
    mintAuthorityActive: null,
    freezeAuthorityActive: null,
    totalSupply: null,
    topHolderPercent: null,
    topFiveHolderPercent: null,
    totalHolders: null,
    recentTxCount: null,
    fetchedAt: new Date().toISOString(),
    source: 'helius',
  }
}
