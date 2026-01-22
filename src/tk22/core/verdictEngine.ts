import { ChainFacts, VerdictResult } from "./types";
import { POLICIES } from "./policies";

export function evaluateToken(facts: ChainFacts): VerdictResult {
  const reasons: string[] = [];

  if (facts.mintAuthorityActive !== false) {
    reasons.push("Mint authority active or unknown");
  }

  if (facts.freezeAuthorityActive !== false) {
    reasons.push("Freeze authority active or unknown");
  }

  if (
    facts.topHolderPercent !== null &&
    facts.topHolderPercent > POLICIES.FAIL.TOP_HOLDER_PERCENT
  ) {
    reasons.push("Top holder exceeds fail threshold");
  }

  if (reasons.length > 0) {
    return {
      token: facts.mint,
      verdict: "FAIL_CLOSED",
      confidence: 90,
      signals: facts,
      reasoning: reasons,
      recommendation: "DO NOT TOUCH",
    };
  }

  return {
    token: facts.mint,
    verdict: "SAFE",
    confidence: 70,
    signals: facts,
    reasoning: ["No structural risks detected on-chain"],
    recommendation: "STRUCTURALLY SAFE",
  };
}
