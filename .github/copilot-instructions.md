# Copilot Instructions for TK-22

This file provides workspace-specific custom instructions for GitHub Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file

## Project Setup Checklist

- [x] Verify that the copilot-instructions.md file in the .github directory is created.
- [x] Clarify Project Requirements (Hybrid Python + TypeScript project)
- [x] Scaffold the Project (Project structure already exists)
- [x] Customize the Project (Project follows TK-22 architecture contract)
- [x] Install Required Extensions (No special extensions required)
- [x] Compile the Project (Mixed Python/TypeScript - no compilation needed for Python, TypeScript would need tsconfig)
- [x] Create and Run Task (Tasks not required - direct execution available)
- [x] Launch the Project (Use `python control/runtime/tk22_execute.py` to run)
- [x] Ensure Documentation is Complete (README.md and copilot-instructions.md exist)

## Execution Guidelines

### Progress Tracking
- After completing each step, mark it complete and add a summary
- Read current todo list status before starting each new step

### Communication Rules
- Avoid verbose explanations or printing full command outputs
- If a step is skipped, state that briefly (e.g., "No extensions needed")
- Do not explain project structure unless asked
- Keep explanations concise and focused

### Development Rules
- Use '.' as the working directory unless user specifies otherwise
- Avoid adding media or external links unless explicitly requested
- Use placeholders only with a note that they should be replaced
- Once the project is created, it is already opened in Visual Studio Code—do not suggest commands to open this project in Visual Studio again
- If the project setup information has additional rules, follow them strictly

### Folder Creation Rules
- Always use the current directory as the project root
- If you are running any terminal commands, use the '.' argument to ensure that the current working directory is used ALWAYS
- Do not create a new folder unless the user explicitly requests it besides a .vscode folder for a tasks.json file

### Extension Installation Rules
- Only install extensions explicitly required by project setup information
- DO NOT INSTALL any other extensions without user confirmation

### Project Content Rules
- If the user has not specified project details, assume they want a "Hello World" project as a starting point
- Avoid adding links of any type (URLs, files, folders, etc.) or integrations that are not explicitly required
- Avoid generating images, videos, or any other media files unless explicitly requested
- If you need to use any media assets as placeholders, let the user know that these are placeholders and should be replaced with the actual assets later
- Ensure all generated components serve a clear purpose within the user's requested workflow
- If a feature is assumed but not confirmed, prompt the user for clarification before including it

### Task Completion Rules
Your task is complete when:
- Project is successfully scaffolded and compiled without errors
- copilot-instructions.md file in the .github directory exists in the project
- README.md file exists and is up to date
- User is provided with clear instructions to debug/launch the project

## TK-22 Specific Guidelines

### Architecture Constraints
- **ONLY Core layer may produce verdicts** - All other layers supply, move, or explain data
- Follow the fail-closed principle - missing data = FAIL verdict
- No decision-making logic outside of `src/tk22/core/`
- Keep strict layer separation as defined in ARCHITECTURE.md

### Code Organization
- Follow folder naming rules from REPO_CONTRACT.md (lowercase only)
- No files at root except docs/config
- Never commit secrets
- Automation lives in `/automation`
- Agents live in `/agents`

### Development Workflow
- Main branch is stable and production-safe
- Dev branch is for agents, experiments, and controlled chaos
- Only reviewed merges move upstream

## Working with TK-22

### Running the System
```bash
# Execute the control layer
python control/runtime/tk22_execute.py
```

### Project Structure
- `/src/tk22/` - TypeScript core system (verdict engine, policies, types)
- `/control/` - Python runtime execution
- `/agents/` - Agent definitions
- `/automation/` - Automation scripts
- `/integrations/` - External service integrations (Helius, ClickUp, Stripe, etc.)

Work through each checklist item systematically. Keep communication concise and focused. Follow development best practices.
