# Crystal Clear Data - Copilot Instructions

## Core Context
I operate multiple digital businesses: TheDiscoBass (NFT/music), Prompt Parlay (AI sports betting), the_steele_zone (content), Family Wealth Engine (real estate), plus tk-22, tk-22-ui, cognitive-ai, and disco-agent-saas. I code in Python, use Supabase databases, n8n automation, Claude MCP for AI. I value direct, action-oriented solutions over theory.

## Execution Rules (CRITICAL)

### ALWAYS
- Run operations through VS Code tasks in `.vscode/tasks.json`
- Start paths from `${workspaceFolder}` root
- Load env vars from `.env` only
- Check `.agents/authority.md` before multi-step ops
- Use Python 3.11+ with type hints
- Prefer f-strings over .format()
- Use `python-dotenv` for config
- Import: `from supabase import create_client, Client`
- Use `requests` library for HTTP
- Add docstrings to functions

### NEVER
- Execute shell commands outside defined tasks
- Use `os.system()` or `subprocess` without approval
- Modify files outside workspace
- Commit secrets, API keys, `.env` files
- Use `eval()` or `exec()` on untrusted input
- Install without updating `requirements.txt`
- Guess at API credentials

## When I Say "Run everything safely"
→ Execute VS Code task: "Run Everything Safely"
→ NOT freeform command
→ Only approved multi-step entry point per `.vscode/tasks.json`

## Code Style

### Python
```python
def fetch_properties(county: str) -> list[dict]:
    """Fetch properties from Supabase."""
    supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))
    response = supabase.table("properties").select("*").eq("county", county).execute()
    return response.data
```

### TypeScript
```typescript
interface PropertyQuery {
  county: string;
}

async function fetchProperties(query: PropertyQuery): Promise<Property[]> {
  const { data } = await supabase
    .from('properties')
    .select('*')
    .eq('county', query.county);
  return data;
}
```

## Project Structure
- `/backend` - Python FastAPI services
- `/frontend` - Next.js/React UI
- `/automation` - n8n workflows
- `/integrations` - External API connectors
- `/ops` - Deployment configs

## Key Files
- `.vscode/tasks.json` - All approved automation
- `.agents/authority.md` - Agent permissions
- `REPO_CONTRACT.md` - Development rules
- `.env.example` - Required environment variables

## Common Patterns
- Always validate Supabase connections before operations
- Use environment-specific configs (dev/staging/prod)
- Log all external API calls
- Handle rate limits gracefully
- Write tests for business logic

## Questions to Ask
- "Should this be a VS Code task?"
- "Do I need to check agent authority?"
- "Are there security implications?"
- "Is this covered in REPO_CONTRACT.md?"
