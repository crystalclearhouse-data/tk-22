# Solana Token Safety Scanner

**A terminal-based tool that analyzes Solana tokens for safety risks and provides clear verdicts.**

Built on TK-22's fail-closed architecture, this scanner examines on-chain token data to identify structural risks that could lead to loss of funds.

## 🚀 Quick Start

### Installation

1. **Install Python 3.8+** (if not already installed)
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run a scan:**
   ```bash
   python solana_scanner.py <TOKEN_MINT_ADDRESS>
   ```

### Example Usage

```bash
# Scan USDC (should be SAFE)
python solana_scanner.py EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v

# Scan SOL (wrapped SOL, should be SAFE)
python solana_scanner.py So11111111111111111111111111111111111111112

# Use custom RPC endpoint
python solana_scanner.py <MINT_ADDRESS> --rpc https://api.devnet.solana.com
```

## 📊 Understanding Results

The scanner provides three possible verdicts:

### ✅ SAFE

- No major structural risks detected
- Both mint and freeze authorities are typically revoked
- Standard token behavior expected

### ⚠️ RISKY

- Elevated risk factors present
- May include: active mint authority, transfer fees, complex extensions
- Proceed with caution and understand the risks

### 🚨 TRAP

- High risk of fund loss
- May include: freeze authority active, non-transferable tokens
- **Strongly recommend avoiding these tokens**

## 🔍 What This Tool Checks

### Token Program Detection

- **SPL Token** - Standard Solana token program
- **Token-2022** - New token program with advanced features

### Risk Factors Analyzed

#### Critical Risks (TRAP):

- **Freeze Authority Active** - Token issuer can freeze your tokens
- **Non-Transferable** - Tokens cannot be moved once received
- **Unknown dangerous extensions**

#### Elevated Risks (RISKY):

- **Mint Authority Active** - Issuer can create unlimited new tokens (inflation)
- **Transfer Fees** - Fees charged on every transfer
- **Complex Extensions** - Advanced Token-2022 features with unknown implications

#### Safety Indicators (SAFE):

- **Authorities Revoked** - No central control over token behavior
- **Standard Structure** - Well-understood token mechanics
- **No Risky Extensions** - Simple, predictable behavior

## ⚠️ Important Disclaimers

### What This Tool DOES:

- ✅ Analyzes on-chain token structure and permissions
- ✅ Identifies technical risks in token design
- ✅ Checks for dangerous Token-2022 extensions
- ✅ Provides fail-safe analysis (when in doubt, warns of risk)

### What This Tool DOES NOT Do:

- ❌ **Check token price or market data**
- ❌ **Verify team legitimacy or social media presence**
- ❌ **Analyze smart contract code beyond basic structure**
- ❌ **Provide investment or financial advice**
- ❌ **Guarantee token safety or legitimacy**
- ❌ **Check for rug pull risks or exit scams**
- ❌ **Validate token utility or use case**

### Critical Understanding:

- **A "SAFE" verdict only means no structural risks were detected**
- **Tokens can still lose value, be abandoned, or fail for other reasons**
- **Always do your own research before investing**
- **This tool is for educational and risk assessment purposes only**

## 🛠 Technical Details

### Architecture

Built on TK-22's fail-closed architecture:

- **Deterministic Analysis** - Same input always produces same output
- **Fail-Safe Design** - When uncertain, warns of risk
- **No External Dependencies** - Analysis based purely on blockchain data
- **Transparent Logic** - Clear reasoning provided for all verdicts

### Data Sources

- **Solana RPC** - Direct blockchain data access
- **Token Mint Accounts** - Official token configuration
- **Token-2022 Extensions** - Advanced feature detection

### Supported Networks

- **Mainnet** (default)
- **Devnet** (via --rpc flag)
- **Testnet** (via --rpc flag)
- **Custom RPC endpoints**

## 📞 Support & Services

### Manual Token Analysis Service

Need a deeper analysis or have questions about a specific token?

**Contact us for professional token analysis:**

- 📧 Email: [Your Contact Email]
- 💬 Telegram: [Your Telegram]
- 🐦 Twitter: [Your Twitter]

**Professional Analysis Includes:**

- Detailed risk assessment report
- Market context and token history
- Team and project verification
- Custom risk scoring
- Investment recommendations

_Starting at $50 per token analysis_

### Bulk Analysis

Need to analyze multiple tokens? We offer:

- Portfolio risk assessment
- Batch token scanning
- Custom risk policies
- Integration support

## 🔧 Troubleshooting

### Common Issues

**"Invalid mint address format"**

- Ensure you're using the correct Solana mint address
- Addresses should be 32-44 characters, base58 encoded

**"Token not found or invalid"**

- The mint address may not exist
- Check if you're using the correct network (mainnet vs devnet)
- Verify the address is actually a token mint

**"Failed to connect to Solana RPC"**

- Check your internet connection
- Try a different RPC endpoint with --rpc flag
- Some RPC endpoints may have rate limits

**"Network timeout"**

- Solana network may be congested
- Try again in a few minutes
- Use a different RPC endpoint

### Getting Help

If you encounter persistent issues:

1. Check that all dependencies are installed correctly
2. Verify your Python version (3.8+ required)
3. Try with a known working token address first
4. Contact support with the full error message

## 📄 License

This tool is provided as-is for educational and risk assessment purposes.

**No warranty or guarantee is provided. Use at your own risk.**

---

_Built with TK-22 fail-closed architecture for maximum reliability_
