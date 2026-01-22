// src/tk22/apis/scan.ts

import { evaluateVerdict } from '../core/verdictEngine';
import { ChainFacts } from '../core/types';

/**
 * scanToken
 *
 * Transport-only API.
 * No defaults. No retries. No interpretation.
 * Returns core verdict verbatim.
 */
export async function scanToken(facts: ChainFacts) {
  return evaluateVerdict(facts);
}
