import { scanToken } from '../scan';

describe('TK22 Scan API (verbatim contract)', () => {
  it('returns FAIL_CLOSED when facts are missing (fail-closed)', async () => {
    const result = await scanToken({
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
    });

    expect(result.verdict).toBe('FAIL_CLOSED');
    expect(result.reasoning.length).toBeGreaterThan(0);
  });
});
