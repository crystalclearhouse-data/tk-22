import { evaluateVerdict } from '../verdictEngine';
import { ChainFacts } from '../types';

describe('TK22 Golden Fail-Closed Invariant', () => {
  it('FAILS when required adapter data is missing', () => {
    // Simulate adapter failure / missing data
    const incompleteFacts: ChainFacts = {
      liquidityUSD: null,
      holderCount: null,
      mintAuthorityRenounced: null,
      freezeAuthorityRenounced: null,
      ageInDays: null,
    };

    const result = evaluateVerdict(incompleteFacts);

    expect(result.verdict).toBe('FAIL');
    expect(result.reasons.length).toBeGreaterThan(0);
    expect(result.reasons).toContain(
      expect.stringMatching(/missing|required|undefined/i)
    );
  });
});
