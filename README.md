# Canva MCP Implementation

This repository implements a Canva MCP (Model Context Protocol) integration that allows AI agents to create designs in Canva accounts programmatically.

## What This Is

Based on [Canva's official MCP documentation](https://canva.dev/docs/apps/mcp/), this is a standardized protocol that gives AI agents access to Canva's design capabilities through:

- Design generation from text descriptions
- Design editing and management
- Asset upload and brand management
- Export in multiple formats

## Configuration

### For Cursor IDE

Copy `.cursor/mcp.json` into your Cursor config directory:

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

### For VS Code

Copy `.vscode/mcp.json` into your VS Code workspace:

```json
{
  "servers": {
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

## Available MCP Tools

| Tool | Description | Rate Limit | Plan Required |
|------|------------- estuvo |-----------|---------------|
| `generate-design` | Create design candidates from text | 20 req/min | All plans |
| `generate-design-structured` | Create controlled layouts | 20 req/min | All plans |
| `create-design-from-candidate` | Create real design from candidate | 20 req/min | All plans |
| `search-designs` | Search your design library | 100 req/min | All plans |
| `search-brand-templates` | Search brand templates | 100 req/min | Pro+ |
| `list-brand-kits` | List brand kits | 100 req/min | Pro+ |
| `export-design` | Export design to various formats | 20 req/min | All plans* |
| `resize-design` | Resize design to new dimensions | 20 req/min | Pro+ |
| `upload-asset-from-url` | Upload assets from URLs | 30 req/min | All plans |

*Standard quality export; Pro quality with lossless PNG, transparent backgrounds, and premium element export for Pro and above

## Implementation Steps

1. **Configure MCP Client**: Add the JSON config to your AI assistant
2. **Authentication**: When the agent connects, it will prompt you to sign in to Canva and authorize access
3. **Verify Connection**: Test with `search-designs` to ensure everything works
4. **Design Creation**: Use `generate-design` or `generate-design-structured` to create designs
5. **Export**: Use `export-design` to get the final design

## Important Notes

- **Individual Authentication**: Each user must authenticate individually via OAuth
- **Plan Requirements**: Some features require Canva Pro or above (brand templates, resizing)
- **AI Credits**: Some AI-powered actions use monthly Canva AI allowance
- **Rate Limits**: Follow the documented rate limits for each tool

## Documentation

- [Plan Document](plan.md) - Detailed step-by-step implementation plan
- [Canva Help Center](https://www.canva.com/help/mcp-agent-setup/) - End-user setup guide
- [Canva Developer Documentation](https://canva.dev/docs/apps/mcp/) - Developer API docs

## Next Steps

Choose one of these options:

1. **Start with a simple agent script** that tests Canva MCP connection
2. **Walk through Canva Developer Portal setup** (creating an app, enabling MCP, getting OAuth credentials)
3. **Create an example implementation** that shows how the agents create designs