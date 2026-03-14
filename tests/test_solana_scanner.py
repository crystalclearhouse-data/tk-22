"""
Tests for Solana Token Safety Scanner

These tests validate the core analysis logic using mock data.
Real blockchain integration tests are in test_token_examples.py
"""

import unittest
from datetime import datetime
from src.tk22.core.token_analyzer import analyze_solana_token, TokenAnalysisResult


class TestTokenAnalyzer(unittest.TestCase):
    """Test the core token analysis logic."""
    
    def test_safe_spl_token(self):
        """Test analysis of a safe SPL token."""
        token_data = {
            "mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            "program_type": "spl-token",
            "mint_authority_active": False,
            "freeze_authority_active": False,
            "supply": 1000000000,
            "decimals": 6,
            "is_initialized": True,
            "extensions": [],
            "fetched_at": datetime.utcnow().isoformat(),
            "source": "test"
        }
        
        result = analyze_solana_token(token_data)
        
        self.assertEqual(result.verdict, "SAFE")
        self.assertEqual(result.program_type, "spl-token")
        self.assertIn("revoked", " ".join(result.reasoning).lower())
    
    def test_risky_token_with_mint_authority(self):
        """Test token with active mint authority."""
        token_data = {
            "mint": "test_mint",
            "program_type": "spl-token", 
            "mint_authority_active": True,
            "freeze_authority_active": False,
            "supply": 1000000,
            "decimals": 9,
            "is_initialized": True,
            "extensions": [],
            "fetched_at": datetime.utcnow().isoformat(),
            "source": "test"
        }
        
        result = analyze_solana_token(token_data)
        
        self.assertEqual(result.verdict, "RISKY")
        self.assertIn("mint authority", " ".join(result.reasoning).lower())
    
    def test_trap_token_with_freeze_authority(self):
        """Test token with active freeze authority."""
        token_data = {
            "mint": "test_mint",
            "program_type": "spl-token",
            "mint_authority_active": False,
            "freeze_authority_active": True,
            "supply": 1000000,
            "decimals": 9,
            "is_initialized": True,
            "extensions": [],
            "fetched_at": datetime.utcnow().isoformat(),
            "source": "test"
        }
        
        result = analyze_solana_token(token_data)
        
        self.assertEqual(result.verdict, "TRAP")
        self.assertIn("freeze", " ".join(result.reasoning).lower())
    
    def test_token2022_with_transfer_fees(self):
        """Test Token-2022 with transfer fees (should be RISKY)."""
        token_data = {
            "mint": "test_mint",
            "program_type": "token-2022",
            "mint_authority_active": False,
            "freeze_authority_active": False,
            "supply": 1000000,
            "decimals": 6,
            "is_initialized": True,
            "extensions": [
                {
                    "type": 1,
                    "name": "transfer_fee_config",
                    "length": 32,
                    "data": "base64data"
                }
            ],
            "fetched_at": datetime.utcnow().isoformat(),
            "source": "test"
        }
        
        result = analyze_solana_token(token_data)
        
        self.assertEqual(result.verdict, "RISKY")
        self.assertIn("transfer fee", " ".join(result.reasoning).lower())
    
    def test_token2022_non_transferable(self):
        """Test Token-2022 with non-transferable extension (should be TRAP)."""
        token_data = {
            "mint": "test_mint",
            "program_type": "token-2022",
            "mint_authority_active": False,
            "freeze_authority_active": False,
            "supply": 1000000,
            "decimals": 6,
            "is_initialized": True,
            "extensions": [
                {
                    "type": 5,
                    "name": "non_transferable",
                    "length": 0,
                    "data": ""
                }
            ],
            "fetched_at": datetime.utcnow().isoformat(),
            "source": "test"
        }
        
        result = analyze_solana_token(token_data)
        
        self.assertEqual(result.verdict, "TRAP")
        self.assertIn("non-transferable", " ".join(result.reasoning).lower())
    
    def test_unknown_program_type(self):
        """Test token with unknown program type (should be TRAP)."""
        token_data = {
            "mint": "test_mint",
            "program_type": "unknown",
            "mint_authority_active": None,
            "freeze_authority_active": None,
            "supply": None,
            "decimals": None,
            "is_initialized": None,
            "extensions": [],
            "fetched_at": datetime.utcnow().isoformat(),
            "source": "test"
        }
        
        result = analyze_solana_token(token_data)
        
        self.assertEqual(result.verdict, "TRAP")
        self.assertIn("unknown", " ".join(result.reasoning).lower())
    
    def test_uninitialized_token(self):
        """Test uninitialized token (should be TRAP)."""
        token_data = {
            "mint": "test_mint",
            "program_type": "spl-token",
            "mint_authority_active": False,
            "freeze_authority_active": False,
            "supply": 0,
            "decimals": 0,
            "is_initialized": False,
            "extensions": [],
            "fetched_at": datetime.utcnow().isoformat(),
            "source": "test"
        }
        
        result = analyze_solana_token(token_data)
        
        self.assertEqual(result.verdict, "TRAP")
        self.assertIn("not initialized", " ".join(result.reasoning).lower())


class TestTokenAnalysisResult(unittest.TestCase):
    """Test the TokenAnalysisResult class."""
    
    def test_result_creation(self):
        """Test creating a TokenAnalysisResult."""
        result = TokenAnalysisResult(
            mint="test_mint",
            verdict="SAFE",
            confidence=85,
            signals={"test": True},
            reasoning=["Test reason"],
            recommendation="Test recommendation",
            program_type="spl-token"
        )
        
        self.assertEqual(result.mint, "test_mint")
        self.assertEqual(result.verdict, "SAFE")
        self.assertEqual(result.confidence, 85)
        self.assertEqual(result.program_type, "spl-token")
        self.assertIsNotNone(result.analyzed_at)


if __name__ == "__main__":
    unittest.main()

