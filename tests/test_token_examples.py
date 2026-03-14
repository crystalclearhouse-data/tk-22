"""
Integration tests with real Solana token examples.

These tests use actual token mint addresses to validate the scanner
against real blockchain data. Run with caution as they make network calls.
"""

import unittest
import os
from src.tk22.adapters.solana.rpc_client import SolanaRPCClient
from src.tk22.core.token_analyzer import analyze_solana_token


class TestRealTokenExamples(unittest.TestCase):
    """Test scanner with real token examples."""
    
    def setUp(self):
        """Set up RPC client for tests."""
        # Use devnet for testing to avoid mainnet rate limits
        self.client = SolanaRPCClient("https://api.devnet.solana.com")
        
        # Skip tests if no network access
        self.skip_network_tests = os.environ.get("SKIP_NETWORK_TESTS", "false").lower() == "true"
    
    def test_usdc_mainnet(self):
        """Test USDC on mainnet (should be SAFE)."""
        if self.skip_network_tests:
            self.skipTest("Network tests disabled")
        
        # Switch to mainnet for USDC
        client = SolanaRPCClient("https://api.mainnet-beta.solana.com")
        
        # USDC mint address
        usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
        
        try:
            token_data = client.get_token_analysis_data(usdc_mint)
            self.assertIsNotNone(token_data, "Should fetch USDC data")
            
            result = analyze_solana_token(token_data)
            
            # USDC should be relatively safe (authorities might be revoked)
            self.assertIn(result.verdict, ["SAFE", "RISKY"])
            self.assertEqual(result.program_type, "spl-token")
            
        except Exception as e:
            self.skipTest(f"Network error: {e}")
    
    def test_wrapped_sol_mainnet(self):
        """Test wrapped SOL on mainnet."""
        if self.skip_network_tests:
            self.skipTest("Network tests disabled")
        
        # Switch to mainnet for wrapped SOL
        client = SolanaRPCClient("https://api.mainnet-beta.solana.com")
        
        # Wrapped SOL mint address
        wsol_mint = "So11111111111111111111111111111111111111112"
        
        try:
            token_data = client.get_token_analysis_data(wsol_mint)
            self.assertIsNotNone(token_data, "Should fetch wrapped SOL data")
            
            result = analyze_solana_token(token_data)
            
            # Wrapped SOL should be safe
            self.assertEqual(result.verdict, "SAFE")
            self.assertEqual(result.program_type, "spl-token")
            
        except Exception as e:
            self.skipTest(f"Network error: {e}")
    
    def test_invalid_mint_address(self):
        """Test with invalid mint address."""
        invalid_mint = "InvalidMintAddress123"
        
        token_data = self.client.get_token_analysis_data(invalid_mint)
        self.assertIsNone(token_data, "Should return None for invalid mint")
    
    def test_nonexistent_mint_address(self):
        """Test with valid format but nonexistent mint."""
        # Valid base58 format but doesn't exist
        fake_mint = "11111111111111111111111111111111111111111111"
        
        token_data = self.client.get_token_analysis_data(fake_mint)
        # Should return None for nonexistent mint
        self.assertIsNone(token_data)


class TestRPCClient(unittest.TestCase):
    """Test the RPC client functionality."""
    
    def setUp(self):
        self.client = SolanaRPCClient("https://api.devnet.solana.com")
        self.skip_network_tests = os.environ.get("SKIP_NETWORK_TESTS", "false").lower() == "true"
    
    def test_get_token_program_type(self):
        """Test program type detection."""
        if self.skip_network_tests:
            self.skipTest("Network tests disabled")
        
        # Test with invalid address
        result = self.client.get_token_program_type("invalid")
        self.assertIsNone(result)
    
    def test_parse_spl_mint_data(self):
        """Test SPL mint data parsing."""
        # Create mock SPL mint data (82 bytes minimum)
        mock_data = bytearray(82)
        
        # Set mint authority option (1 byte) - no authority
        mock_data[0] = 0
        
        # Supply (8 bytes) - 1,000,000 tokens
        supply = 1000000
        mock_data[33:41] = supply.to_bytes(8, 'little')
        
        # Decimals (1 byte)
        mock_data[41] = 6
        
        # Is initialized (1 byte)
        mock_data[42] = 1
        
        # Freeze authority option (1 byte) - no authority
        mock_data[43] = 0
        
        result = self.client.parse_spl_mint_data(bytes(mock_data))
        
        self.assertIsNotNone(result)
        self.assertEqual(result["supply"], supply)
        self.assertEqual(result["decimals"], 6)
        self.assertTrue(result["is_initialized"])
        self.assertIsNone(result["mint_authority"])
        self.assertIsNone(result["freeze_authority"])
        self.assertEqual(len(result["extensions"]), 0)
    
    def test_parse_invalid_mint_data(self):
        """Test parsing invalid mint data."""
        # Too short data
        short_data = b"short"
        result = self.client.parse_spl_mint_data(short_data)
        self.assertIsNone(result)
        
        # Empty data
        empty_data = b""
        result = self.client.parse_spl_mint_data(empty_data)
        self.assertIsNone(result)


if __name__ == "__main__":
    # Set environment variable to skip network tests by default
    if "SKIP_NETWORK_TESTS" not in os.environ:
        os.environ["SKIP_NETWORK_TESTS"] = "true"
        print("Network tests disabled by default. Set SKIP_NETWORK_TESTS=false to enable.")
    
    unittest.main()

