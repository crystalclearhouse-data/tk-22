import { scanToken } from '../scan';

describe('TK22 Scan API (verbatim contract)', () => {
  it('returns FAIL when facts are missing (fail-closed)', async () => {
    const result = await scanToken({
      liquidityUSD: null,
      holderCount: null,
      mintAuthorityRenounced: null,
      freezeAuthorityRenounced: null,
      ageInDays: null,
    });

    expect(result.verdict).toBe('FAIL');
    expect(result.reasons.length).toBeGreaterThan(0);
  });
});
