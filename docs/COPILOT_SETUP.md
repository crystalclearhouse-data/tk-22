# GitHub Copilot Agent Mode Setup Guide

This guide explains how to set up and use GitHub Copilot Agent Mode in the TK-22 repository.

## Prerequisites

1. **GitHub Copilot Subscription**: You must have an active GitHub Copilot subscription (Individual, Business, or Enterprise).
2. **Visual Studio Code**: Version 1.85 or later.
3. **GitHub Copilot Extension**: Install from the VS Code marketplace.

## Setup Instructions

### Step 1: Install GitHub Copilot Extension

1. Open Visual Studio Code
2. Go to Extensions (⌘+Shift+X on macOS, Ctrl+Shift+X on Windows/Linux)
3. Search for "GitHub Copilot"
4. Click "Install" on the official GitHub Copilot extension
5. Also install "GitHub Copilot Chat" extension for enhanced features

### Step 2: Authenticate with GitHub

1. After installation, VS Code will prompt you to sign in to GitHub
2. Click the GitHub Copilot icon in the status bar (bottom right)
3. Follow the authentication flow to authorize Copilot
4. Complete the device code verification in your browser

### Step 3: Verify Configuration

The repository includes pre-configured Copilot settings in `.vscode/settings.json`:

```json
{
  "github.copilot.enable": {
    "*": true
  },
  "github.copilot.editor.enableAutoCompletions": true,
  "github.copilot.chat.useProjectTemplates": true
}
```

These settings enable:
- Copilot across all file types
- Automatic code completions
- Project-aware chat responses

### Step 4: Restart VS Code

After installation and authentication:
1. Save all open files
2. Restart VS Code (Command Palette → "Reload Window" or fully quit and reopen)
3. The Copilot icon should show as active in the status bar

## Features Available

### 1. Inline Code Suggestions
- Type code and Copilot will suggest completions
- Press Tab to accept suggestions
- Press Esc to dismiss

### 2. Copilot Chat
- Open with ⌘+I (macOS) or Ctrl+I (Windows/Linux)
- Ask questions about the codebase
- Request code generation or refactoring
- Get explanations of existing code

### 3. Agent Mode Features
With the current configuration:
- **Context-Aware Suggestions**: Copilot understands the TK-22 architecture
- **Project Templates**: Responses are tailored to this repository's patterns
- **Multi-Language Support**: Works across Python, JavaScript, TypeScript, YAML, and Markdown

## Usage Tips

### For TK-22 Development

1. **Architecture Compliance**: When asking Copilot to generate code, mention the fail-closed design principles from [`../ARCHITECTURE.md`](../ARCHITECTURE.md) to ensure compliance. For example: "Generate a Core verdict function following the fail-closed design pattern."

2. **Layer-Specific Development**: Mention which layer you're working in:
   - "Generate a Core verdict function"
   - "Create an Adapter for fetching Solana data"
   - "Write a Service to orchestrate these adapters"

3. **Testing**: Ask Copilot to generate tests that follow the repository's testing patterns.

### Best Practices

- **Be Specific**: Provide context about what you're building
- **Reference Existing Code**: Ask Copilot to follow patterns from existing files
- **Review Suggestions**: Always review AI-generated code for correctness and security
- **Iterate**: If a suggestion isn't quite right, refine your prompt

## Troubleshooting

### Copilot Not Working

1. Check the status bar icon - it should show a checkmark
2. Verify authentication: Click the Copilot icon → "Check Status"
3. Ensure your subscription is active
4. Try signing out and back in

### No Suggestions Appearing

1. Verify Copilot is enabled in settings
2. Check that auto-completions are enabled
3. Restart the Language Server: Command Palette → "Developer: Reload Window"

### Configuration Issues

1. Verify `.vscode/settings.json` is valid JSON
2. Check for conflicting extensions
3. Review VS Code's Output panel for errors

## Security Considerations

- **Never commit secrets**: Copilot suggestions may include placeholders for API keys
- **Review all code**: AI suggestions should be reviewed for security vulnerabilities
- **Architecture compliance**: Ensure generated code follows TK-22's fail-closed design
- **Data privacy**: Be aware that code context is sent to GitHub's servers

## Additional Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [VS Code Copilot Guide](https://code.visualstudio.com/docs/editor/artificial-intelligence)
- TK-22 Architecture: See [`../ARCHITECTURE.md`](../ARCHITECTURE.md)
- Repository Contract: See [`../REPO_CONTRACT.md`](../REPO_CONTRACT.md)

## Support

For issues with:
- **Copilot itself**: Contact GitHub Support
- **TK-22 configuration**: Open an issue in this repository
- **Architecture questions**: Reference [`../ARCHITECTURE.md`](../ARCHITECTURE.md) or ask in team channels
