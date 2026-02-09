import { evaluateVerdict } from '../verdictEngine';
import { ChainFacts } from '../types';

describe('TK22 Golden Fail-Closed Invariant', () => {
  it('FAILS when required adapter data is missing', () => {
    // Simulate adapter failure / missing data
    const incompleteFacts: ChainFacts = {
      mint: 'test-mint-address',
      liquidityUSD: null,
      holderCount: null,
      mintAuthorityRenounced: null,
      freezeAuthorityRenounced: null,
      ageInDays: null,
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

    const result = evaluateVerdict(incompleteFacts);

    expect(result.verdict).toBe('FAIL_CLOSED');
    expect(result.reasoning.length).toBeGreaterThan(0);
    expect(result.reasoning).toContain(
      expect.stringMatching(/authority|unknown/i)
    );
  });
});
