#!/usr/bin/env python3
"""
Solana Token Safety Scanner - TK-22 MVP

A terminal-based tool that scans Solana token mints and outputs clear safety verdicts.
Built on TK-22's fail-closed architecture for maximum reliability.

Usage:
    python solana_scanner.py <mint_address>
    python solana_scanner.py --help

Example:
    python solana_scanner.py EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
"""

import sys
import argparse
from datetime import datetime
from typing import Optional

# Import TK-22 components
from src.tk22.adapters.solana.rpc_client import SolanaRPCClient
from src.tk22.core.token_analyzer import analyze_solana_token, format_analysis_output


def validate_mint_address(mint_address: str) -> bool:
    """Validate that the mint address looks like a valid Solana public key."""
    if not mint_address:
        return False
    
    # Basic validation - Solana addresses are base58 encoded, 32-44 chars
    if len(mint_address) < 32 or len(mint_address) > 44:
        return False
    
    # Check for valid base58 characters
    valid_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    return all(c in valid_chars for c in mint_address)


def scan_token(mint_address: str, rpc_url: Optional[str] = None) -> int:
    """
    Scan a Solana token and output safety analysis.
    Returns exit code: 0 for success, 1 for error.
    """
    
    print(f"🔍 Scanning Solana token: {mint_address}")
    print(f"⏰ Started at: {datetime.utcnow().isoformat()}Z")
    print()
    
    # Validate input
    if not validate_mint_address(mint_address):
        print("❌ ERROR: Invalid mint address format")
        print("   Solana mint addresses should be 32-44 character base58 strings")
        return 1
    
    # Initialize RPC client
    try:
        client = SolanaRPCClient(rpc_url or "https://api.mainnet-beta.solana.com")
        print(f"🌐 Connected to: {client.rpc_url}")
        print()
    except Exception as e:
        print(f"❌ ERROR: Failed to connect to Solana RPC")
        print(f"   {str(e)}")
        return 1
    
    # Fetch token data
    print("📡 Fetching token data from blockchain...")
    try:
        token_data = client.get_token_analysis_data(mint_address)
        if not token_data:
            print("❌ ERROR: Token not found or invalid")
            print("   This could mean:")
            print("   • The mint address doesn't exist")
            print("   • The account is not a token mint")
            print("   • Network connectivity issues")
            return 1
            
        # Add timestamp
        token_data["fetched_at"] = datetime.utcnow().isoformat()
        
    except Exception as e:
        print(f"❌ ERROR: Failed to fetch token data")
        print(f"   {str(e)}")
        return 1
    
    # Analyze token safety
    print("🔬 Analyzing token safety...")
    try:
        analysis_result = analyze_solana_token(token_data)
    except Exception as e:
        print(f"❌ ERROR: Failed to analyze token")
        print(f"   {str(e)}")
        return 1
    
    # Output results
    print()
    print(format_analysis_output(analysis_result))
    
    # Return appropriate exit code based on verdict
    if analysis_result.verdict == "SAFE":
        return 0
    elif analysis_result.verdict == "RISKY":
        return 0  # Still successful scan, just risky token
    else:  # TRAP
        return 0  # Still successful scan, just dangerous token


def main():
    """Main CLI entry point."""
    
    parser = argparse.ArgumentParser(
        description="Solana Token Safety Scanner - Analyze token safety risks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python solana_scanner.py EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
  python solana_scanner.py So11111111111111111111111111111111111111112 --rpc https://api.devnet.solana.com

Verdicts:
  SAFE  - No major risk factors detected
  RISKY - Elevated risk factors present  
  TRAP  - High risk of loss, avoid

This tool analyzes on-chain data only. It does NOT:
  • Check token price or market data
  • Verify team legitimacy or social presence
  • Analyze smart contract code beyond basic structure
  • Provide investment advice

Always do your own research before interacting with any token.
        """
    )
    
    parser.add_argument(
        "mint_address",
        help="Solana token mint address to analyze"
    )
    
    parser.add_argument(
        "--rpc",
        help="Custom Solana RPC URL (default: mainnet-beta)",
        default="https://api.mainnet-beta.solana.com"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="TK-22 Solana Scanner v1.0.0"
    )
    
    # Parse arguments
    if len(sys.argv) == 1:
        parser.print_help()
        return 1
        
    args = parser.parse_args()
    
    # Run scan
    try:
        return scan_token(args.mint_address, args.rpc)
    except KeyboardInterrupt:
        print("\n⚠️  Scan interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")
        print("   Please report this issue if it persists")
        return 1


if __name__ == "__main__":
    sys.exit(main())

