import { scanToken } from '../scan';
import { ChainFacts } from '../../core/types';

describe('TK22 Scan API (verbatim contract)', () => {
  it('returns FAIL_CLOSED when facts are missing (fail-closed)', async () => {
    const facts: ChainFacts = {
      mint: 'unknown',
      mintAuthorityActive: null,
      freezeAuthorityActive: null,
      totalSupply: null,
      topHolderPercent: null,
      topFiveHolderPercent: null,
      totalHolders: null,
      recentTxCount: null,
      fetchedAt: new Date().toISOString(),
      source: 'helius',
    };

    const result = await scanToken(facts);

    expect(result.verdict).toBe('FAIL_CLOSED');
    expect(result.reasoning.length).toBeGreaterThan(0);
  });
});
