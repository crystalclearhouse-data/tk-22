"""
Solana RPC Client for TK-22 Token Safety Scanner

This adapter fetches token data from Solana blockchain following TK-22's fail-closed architecture.
No defaults. No retries. No interpretation. Returns raw data or None.
"""

import json
import base64
from typing import Optional, Dict, Any, List
from solana.rpc.api import Client
from solders.pubkey import Pubkey
import requests


class SolanaRPCClient:
    """Solana RPC client that fetches token data without interpretation."""
    
    def __init__(self, rpc_url: str = "https://api.mainnet-beta.solana.com"):
        self.client = Client(rpc_url)
        self.rpc_url = rpc_url
    
    def get_mint_info(self, mint_address: str) -> Optional[Dict[str, Any]]:
        """
        Fetch mint account data from Solana.
        Returns None if mint doesn't exist or fetch fails.
        """
        try:
            pubkey = Pubkey.from_string(mint_address)
            response = self.client.get_account_info(pubkey)
            
            if not response.value:
                return None
                
            account_data = response.value
            if not account_data or not hasattr(account_data, 'data'):
                return None
                
            # Parse the account data - it's already bytes in solders
            data = account_data.data
            
            return {
                "mint": mint_address,
                "owner": str(account_data.owner),
                "executable": account_data.executable,
                "lamports": account_data.lamports,
                "data": data,
                "rent_epoch": account_data.rent_epoch
            }
            
        except Exception as e:
            # Fail closed - return None on any error
            return None
    
    def get_token_program_type(self, mint_address: str) -> Optional[str]:
        """
        Determine if token is SPL Token or Token-2022.
        Returns 'spl-token', 'token-2022', or None.
        """
        mint_info = self.get_mint_info(mint_address)
        if not mint_info:
            return None
            
        owner = mint_info.get("owner")
        
        # SPL Token Program ID
        if owner == "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA":
            return "spl-token"
        # Token-2022 Program ID  
        elif owner == "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb":
            return "token-2022"
        else:
            return None
    
    def parse_spl_mint_data(self, data: bytes) -> Optional[Dict[str, Any]]:
        """Parse SPL token mint account data."""
        try:
            if len(data) < 82:  # Minimum SPL mint size
                return None
                
            # SPL Token mint layout:
            # 0-4: mint_authority_option (4 bytes)
            # 4-36: mint_authority (32 bytes) if option == 1
            # 36-44: supply (8 bytes)
            # 44: decimals (1 byte)
            # 45: is_initialized (1 byte)
            # 46-50: freeze_authority_option (4 bytes)
            # 50-82: freeze_authority (32 bytes) if option == 1
            
            mint_authority_option = int.from_bytes(data[0:4], 'little')
            mint_authority = data[4:36] if mint_authority_option == 1 else None
            
            supply = int.from_bytes(data[36:44], 'little')
            decimals = data[44]
            
            is_initialized = data[45] == 1
            
            freeze_authority_option = int.from_bytes(data[46:50], 'little')
            freeze_authority = data[50:82] if freeze_authority_option == 1 else None
            
            return {
                "mint_authority": base64.b64encode(mint_authority).decode() if mint_authority else None,
                "supply": supply,
                "decimals": decimals,
                "is_initialized": is_initialized,
                "freeze_authority": base64.b64encode(freeze_authority).decode() if freeze_authority else None,
                "extensions": []  # SPL tokens don't have extensions
            }
            
        except Exception:
            return None
    
    def parse_token2022_mint_data(self, data: bytes) -> Optional[Dict[str, Any]]:
        """Parse Token-2022 mint account data including extensions."""
        try:
            if len(data) < 82:
                return None
                
            # Base mint data (same as SPL)
            mint_authority_option = int.from_bytes(data[0:4], 'little')
            mint_authority = data[4:36] if mint_authority_option == 1 else None
            
            supply = int.from_bytes(data[36:44], 'little')
            decimals = data[44]
            is_initialized = data[45] == 1
            
            freeze_authority_option = int.from_bytes(data[46:50], 'little')
            freeze_authority = data[50:82] if freeze_authority_option == 1 else None
            
            # Parse extensions (Token-2022 specific)
            extensions = []
            if len(data) > 82:
                extensions = self._parse_token2022_extensions(data[82:])
            
            return {
                "mint_authority": base64.b64encode(mint_authority).decode() if mint_authority else None,
                "supply": supply,
                "decimals": decimals,
                "is_initialized": is_initialized,
                "freeze_authority": base64.b64encode(freeze_authority).decode() if freeze_authority else None,
                "extensions": extensions
            }
            
        except Exception:
            return None
    
    def _parse_token2022_extensions(self, extension_data: bytes) -> List[Dict[str, Any]]:
        """Parse Token-2022 extensions from account data."""
        extensions = []
        offset = 0
        
        try:
            while offset < len(extension_data):
                if offset + 4 > len(extension_data):
                    break
                    
                # Extension type (2 bytes) + length (2 bytes)
                ext_type = int.from_bytes(extension_data[offset:offset+2], 'little')
                ext_length = int.from_bytes(extension_data[offset+2:offset+4], 'little')
                
                if offset + 4 + ext_length > len(extension_data):
                    break
                
                ext_data = extension_data[offset+4:offset+4+ext_length]
                
                extension = {
                    "type": ext_type,
                    "length": ext_length,
                    "data": base64.b64encode(ext_data).decode()
                }
                
                # Parse known extension types
                if ext_type == 1:  # Transfer Fee Config
                    extension["name"] = "transfer_fee_config"
                elif ext_type == 2:  # Transfer Fee Amount
                    extension["name"] = "transfer_fee_amount"
                elif ext_type == 3:  # Mint Close Authority
                    extension["name"] = "mint_close_authority"
                elif ext_type == 4:  # Confidential Transfer Mint
                    extension["name"] = "confidential_transfer_mint"
                elif ext_type == 5:  # Non Transferable
                    extension["name"] = "non_transferable"
                elif ext_type == 6:  # Interest Bearing Config
                    extension["name"] = "interest_bearing_config"
                else:
                    extension["name"] = f"unknown_{ext_type}"
                
                extensions.append(extension)
                offset += 4 + ext_length
                
        except Exception:
            # Return partial extensions if parsing fails
            pass
            
        return extensions
    
    def get_token_analysis_data(self, mint_address: str) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive token data for safety analysis.
        Returns structured data or None if fetch fails.
        """
        program_type = self.get_token_program_type(mint_address)
        if not program_type:
            return None
            
        mint_info = self.get_mint_info(mint_address)
        if not mint_info:
            return None
            
        # Parse mint data based on program type
        if program_type == "spl-token":
            parsed_data = self.parse_spl_mint_data(mint_info["data"])
        elif program_type == "token-2022":
            parsed_data = self.parse_token2022_mint_data(mint_info["data"])
        else:
            return None
            
        if not parsed_data:
            return None
            
        return {
            "mint": mint_address,
            "program_type": program_type,
            "mint_authority_active": parsed_data["mint_authority"] is not None,
            "freeze_authority_active": parsed_data["freeze_authority"] is not None,
            "supply": parsed_data["supply"],
            "decimals": parsed_data["decimals"],
            "is_initialized": parsed_data["is_initialized"],
            "extensions": parsed_data["extensions"],
            "fetched_at": None,  # Will be set by caller
            "source": "solana_rpc"
        }
