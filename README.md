# TK-22

TK-22 — Crystal Clear House Locked-core automation repo. main is stable and production-safe; dev is for agents, experiments, and controlled chaos. Only reviewed merges move upstream.

## Overview

TK-22 is a deterministic safety and verdict engine designed to evaluate the safety of blockchain assets based on hard rules and verifiable facts. The system follows a fail-closed architecture where any missing or unclear data results in a FAIL verdict.

## Architecture

The project follows a strict layer model (see [ARCHITECTURE.md](ARCHITECTURE.md) for complete details):

- **Core Layer** (`src/tk22/core/`) - The only decision-making layer with deterministic policy evaluation
- **Adapters Layer** (`src/tk22/adapters/`) - External data acquisition from APIs and blockchain
- **Models Layer** (`src/tk22/models/`) - Type definitions and structural validation
- **Services Layer** (`src/tk22/services/`) - Orchestration and data flow
- **Agent Layer** (`src/tk22/agent/`) - Task automation and coordination
- **APIs Layer** (`src/tk22/apis/`) - HTTP/RPC interfaces
- **Gen Layer** (`src/tk22/gen/`) - Human-facing explanations and narrative
- **Utils Layer** (`src/tk22/utils/`) - Pure helper functions

Additional components:
- **Control Layer** (`control/`) - Python runtime execution and proof generation (separate from core architecture)

## Project Structure

```
/src/tk22/          # TypeScript core system
/control/           # Python runtime execution
/agents/            # Agent definitions
/automation/        # Automation scripts
/integrations/      # External service integrations
/docs/              # Documentation
```

## Getting Started

### Prerequisites

- Python 3.11 or 3.12
- Node.js and npm (for TypeScript components)

### Installation

```bash
# Install Python dependencies (if requirements.txt exists)
pip install -r requirements.txt

# Install TypeScript dependencies (if package.json exists)
npm install
```

### Running the System

```bash
# Execute the control layer
python control/runtime/tk22_execute.py
```

## Development

This project is already set up in Visual Studio Code. See `.github/copilot-instructions.md` for Copilot-specific development guidelines.

## Contributing

Follow the guidelines in [REPO_CONTRACT.md](REPO_CONTRACT.md) to ensure consistency across the repository.
