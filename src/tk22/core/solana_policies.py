"""
Solana Token Safety Policies for TK-22

Defines the rules for determining token safety based on on-chain data.
Following TK-22's fail-closed architecture - when in doubt, fail.
"""

# Risk thresholds and policies
SOLANA_POLICIES = {
    "TRAP": {
        # Conditions that make a token a definite trap
        "non_transferable": True,  # Token-2022 non-transferable extension
        "freeze_authority_active": True,  # Can freeze user tokens
    },
    
    "RISKY": {
        # Conditions that make a token risky but not necessarily a trap
        "mint_authority_active": True,  # Can mint unlimited tokens
        "transfer_fees_enabled": True,  # Token-2022 transfer fees
        "unknown_extensions": True,  # Token-2022 with unknown extensions
    },
    
    "SAFE": {
        # Conditions for a token to be considered safe
        "mint_authority_revoked": True,  # Cannot mint new tokens
        "freeze_authority_revoked": True,  # Cannot freeze tokens
        "no_risky_extensions": True,  # No problematic Token-2022 extensions
    }
}

# Extension type mappings for Token-2022
TOKEN2022_EXTENSION_RISKS = {
    "transfer_fee_config": "RISKY",  # Transfer fees
    "transfer_fee_amount": "RISKY",  # Transfer fees
    "non_transferable": "TRAP",  # Cannot transfer
    "mint_close_authority": "RISKY",  # Can close mint
    "confidential_transfer_mint": "RISKY",  # Privacy features (unknown implications)
    "interest_bearing_config": "RISKY",  # Interest bearing (complex mechanics)
}

def get_extension_risk_level(extension_name: str) -> str:
    """Get risk level for a Token-2022 extension."""
    return TOKEN2022_EXTENSION_RISKS.get(extension_name, "RISKY")  # Unknown = risky

