# Canva MCP Skill for DSH Agents

This skill enables DSH agents to create and manage Canva designs programmatically using the Model Context Protocol (MCP).

## Skill Overview

- **Name**: canva-mcp
- **Type**: MCP-based skill
- **Purpose**: Give DSH agents access to Canva's design capabilities
- **MCP Server**: https://mcp.canva.com/mcp
- **Authentication**: OAuth (user must sign in to Canva)

## Capabilities

| Capability | MCP Tool | Rate Limit | Plan Required |
|------------|----------|------------|---------------|
| Design Generation | `generate-design` | 20 req/min | All plans |
| Design Generation (Structured) | `generate-design-structured` | 20 req/min | All plans |
| Design Search | `search-designs` | 100 req/min | All plans |
| Design Export | `export-design` | 20 req/min | All plans* |
| Asset Upload | `upload-asset-from-url` | 30 req/min | All plans |
| Brand Templates | `search-brand-templates` | 100 req/min | Pro+ |
| Brand Kits | `list-brand-kits` | 100 req/min | Pro+ |
| Design Resize | `resize-design` | 20 req/min | Pro+ |
| Design Editing | `start-editing-transaction` | Varies | All plans |
| Comments | `comment-on-design` | 100 req/min | All plans |

*Standard quality export; Pro quality with lossless PNG, transparent backgrounds, and premium element export for Pro and above

## Setup Instructions

### 1. Configure MCP Client

Add the following to your AI agent's MCP configuration:

```json
{
  "mcpServers": {
    "Canva": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "https://mcp.canva.com/mcp"
      ]
    }
  }
}
```

### 2. Authenticate

When the agent first connects, it will prompt you to:
1. Sign in to Canva
2. Authorize the agent to access your Canva account
3. Grant permissions for the operations needed

### 3. Verify Connection

Test with a read-only operation like `search-designs` before creating anything.

## Usage Examples

### Create a Design

```
"Create an Instagram carousel with 3 slides about AI-powered design tips, brand colors blue and white, modern minimal style"
```

### Search Designs

```
"Search my Canva designs for 'marketing presentation'"
```

### Export a Design

```
"Export my 'Q4 Marketing' design as PNG"
```

### Upload an Asset

```
"Upload this logo to my Canva assets"
```

## Important Notes

1. **Individual Authentication**: Each user must authenticate individually via OAuth
2. **Plan Requirements**: Some features require Canva Pro or above
3. **AI Credits**: Some AI-powered actions use monthly Canva AI allowance
4. **Rate Limits**: Follow the documented rate limits for each tool
5. **Error Handling**: Handle authentication failures, rate limits, and permission errors gracefully

## Documentation

- [Canva Help Center](https://www.canva.com/help/mcp-agent-setup/)
- [Canva Developer Docs](https://canva.dev/docs/apps/mcp/)
- [Plan Document](plan.md)

## Files

- `canva_mcp_client.py` - Python MCP client for Canva
- `create-design.js` - JavaScript example
- `.cursor/mcp.json` - Cursor IDE configuration
- `.vscode/mcp.json` - VS Code configuration
- `skill.json` - Skill metadata