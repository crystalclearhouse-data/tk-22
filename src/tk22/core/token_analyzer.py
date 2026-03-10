"""
Solana Token Safety Analyzer for TK-22

Analyzes Solana token data and produces safety verdicts following TK-22's fail-closed architecture.
This is the core decision-making logic - no external calls, pure deterministic evaluation.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from .solana_policies import SOLANA_POLICIES, get_extension_risk_level


class TokenAnalysisResult:
    """Result of token safety analysis."""
    
    def __init__(self, mint: str, verdict: str, confidence: int, 
                 signals: Dict[str, Any], reasoning: List[str], 
                 recommendation: str, program_type: str):
        self.mint = mint
        self.verdict = verdict  # SAFE, RISKY, TRAP
        self.confidence = confidence  # 0-100
        self.signals = signals
        self.reasoning = reasoning
        self.recommendation = recommendation
        self.program_type = program_type
        self.analyzed_at = datetime.utcnow().isoformat()


def analyze_solana_token(token_data: Dict[str, Any]) -> TokenAnalysisResult:
    """
    Analyze Solana token data and return safety verdict.
    
    This is the core verdict engine for Solana tokens.
    Follows TK-22 fail-closed principle: when in doubt, fail.
    """
    mint = token_data.get("mint", "unknown")
    program_type = token_data.get("program_type", "unknown")
    
    # Initialize analysis state
    reasons = []
    signals = {
        "program_type": program_type,
        "mint_authority_active": token_data.get("mint_authority_active"),
        "freeze_authority_active": token_data.get("freeze_authority_active"),
        "supply": token_data.get("supply"),
        "decimals": token_data.get("decimals"),
        "extensions": token_data.get("extensions", []),
        "is_initialized": token_data.get("is_initialized")
    }
    
    # Fail closed if critical data is missing
    if program_type == "unknown":
        return TokenAnalysisResult(
            mint=mint,
            verdict="TRAP",
            confidence=95,
            signals=signals,
            reasoning=["Unknown or invalid token program"],
            recommendation="DO NOT TOUCH - Cannot determine token type",
            program_type=program_type
        )
    
    if token_data.get("is_initialized") is False:
        return TokenAnalysisResult(
            mint=mint,
            verdict="TRAP", 
            confidence=95,
            signals=signals,
            reasoning=["Token mint is not initialized"],
            recommendation="DO NOT TOUCH - Invalid token state",
            program_type=program_type
        )
    
    # Check for TRAP conditions (highest severity)
    trap_reasons = []
    
    # Freeze authority active = can freeze your tokens
    if token_data.get("freeze_authority_active") is True:
        trap_reasons.append("Freeze authority is active - tokens can be frozen")
    
    # Check Token-2022 extensions for trap conditions
    extensions = token_data.get("extensions", [])
    for ext in extensions:
        ext_name = ext.get("name", "unknown")
        risk_level = get_extension_risk_level(ext_name)
        
        if risk_level == "TRAP":
            if ext_name == "non_transferable":
                trap_reasons.append("Token is non-transferable")
            else:
                trap_reasons.append(f"Dangerous extension: {ext_name}")
    
    # If any trap conditions found, return TRAP verdict
    if trap_reasons:
        return TokenAnalysisResult(
            mint=mint,
            verdict="TRAP",
            confidence=90,
            signals=signals,
            reasoning=trap_reasons,
            recommendation="DO NOT TOUCH - High risk of loss",
            program_type=program_type
        )
    
    # Check for RISKY conditions
    risky_reasons = []
    
    # Mint authority active = can mint unlimited tokens (dilution risk)
    if token_data.get("mint_authority_active") is True:
        risky_reasons.append("Mint authority is active - supply can be inflated")
    
    # Check Token-2022 extensions for risky conditions
    for ext in extensions:
        ext_name = ext.get("name", "unknown")
        risk_level = get_extension_risk_level(ext_name)
        
        if risk_level == "RISKY":
            if ext_name == "transfer_fee_config":
                risky_reasons.append("Transfer fees are enabled")
            elif ext_name == "mint_close_authority":
                risky_reasons.append("Mint can be closed by authority")
            elif ext_name == "confidential_transfer_mint":
                risky_reasons.append("Confidential transfers enabled (complex mechanics)")
            elif ext_name == "interest_bearing_config":
                risky_reasons.append("Interest bearing token (complex mechanics)")
            elif ext_name.startswith("unknown_"):
                risky_reasons.append(f"Unknown extension present: {ext_name}")
            else:
                risky_reasons.append(f"Risky extension: {ext_name}")
    
    # If any risky conditions found, return RISKY verdict
    if risky_reasons:
        return TokenAnalysisResult(
            mint=mint,
            verdict="RISKY",
            confidence=75,
            signals=signals,
            reasoning=risky_reasons,
            recommendation="PROCEED WITH CAUTION - Elevated risk factors",
            program_type=program_type
        )
    
    # Check for SAFE conditions
    safe_reasons = []
    
    # Both authorities revoked is good
    if (token_data.get("mint_authority_active") is False and 
        token_data.get("freeze_authority_active") is False):
        safe_reasons.append("Both mint and freeze authorities are revoked")
    elif token_data.get("mint_authority_active") is False:
        safe_reasons.append("Mint authority is revoked (no inflation risk)")
    elif token_data.get("freeze_authority_active") is False:
        safe_reasons.append("Freeze authority is revoked (no freeze risk)")
    
    # SPL tokens without authorities are generally safer
    if program_type == "spl-token" and not extensions:
        safe_reasons.append("Standard SPL token with no complex features")
    
    # Token-2022 with no risky extensions
    if program_type == "token-2022" and not extensions:
        safe_reasons.append("Token-2022 with no extensions enabled")
    
    # If we have positive safety signals, return SAFE
    if safe_reasons:
        return TokenAnalysisResult(
            mint=mint,
            verdict="SAFE",
            confidence=70,
            signals=signals,
            reasoning=safe_reasons,
            recommendation="STRUCTURALLY SAFE - No major risk factors detected",
            program_type=program_type
        )
    
    # Fail closed - if we can't determine safety, it's risky
    return TokenAnalysisResult(
        mint=mint,
        verdict="RISKY",
        confidence=60,
        signals=signals,
        reasoning=["Unable to determine safety - insufficient data"],
        recommendation="PROCEED WITH CAUTION - Incomplete analysis",
        program_type=program_type
    )


def format_analysis_output(result: TokenAnalysisResult) -> str:
    """Format analysis result for terminal output."""
    
    # Header with verdict
    verdict_emoji = {
        "SAFE": "✅",
        "RISKY": "⚠️", 
        "TRAP": "🚨"
    }
    
    output = []
    output.append("=" * 60)
    output.append(f"SOLANA TOKEN SAFETY ANALYSIS")
    output.append("=" * 60)
    output.append(f"Token: {result.mint}")
    output.append(f"Program: {result.program_type.upper()}")
    output.append("")
    output.append(f"VERDICT: {verdict_emoji.get(result.verdict, '❓')} {result.verdict}")
    output.append(f"Confidence: {result.confidence}%")
    output.append(f"Recommendation: {result.recommendation}")
    output.append("")
    
    # Risk factors
    output.append("ANALYSIS:")
    for reason in result.reasoning:
        output.append(f"  • {reason}")
    output.append("")
    
    # Technical details
    output.append("TECHNICAL DETAILS:")
    output.append(f"  • Mint Authority: {'Active' if result.signals.get('mint_authority_active') else 'Revoked'}")
    output.append(f"  • Freeze Authority: {'Active' if result.signals.get('freeze_authority_active') else 'Revoked'}")
    output.append(f"  • Supply: {result.signals.get('supply', 'Unknown'):,}")
    output.append(f"  • Decimals: {result.signals.get('decimals', 'Unknown')}")
    
    # Extensions (Token-2022)
    extensions = result.signals.get("extensions", [])
    if extensions:
        output.append(f"  • Extensions: {len(extensions)} enabled")
        for ext in extensions:
            ext_name = ext.get("name", "unknown")
            output.append(f"    - {ext_name}")
    else:
        output.append("  • Extensions: None")
    
    output.append("")
    output.append(f"Analysis completed at: {result.analyzed_at}")
    output.append("=" * 60)
    
    return "\n".join(output)

