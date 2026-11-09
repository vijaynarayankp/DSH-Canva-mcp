# Canva MCP for AI Agents - Step-by-Step Plan

## 1. Understand What We're Building

**Canva MCP** is a Model Context Protocol implementation that connects AI assistants (agents) to Canva's design capabilities. It's not a traditional "plugin" but a standardized protocol-based integration that allows agents to programmatically create, edit, and manage Canva designs.

Key distinctions:
- **MCP**: The standardized protocol/interface (Model Context Protocol)
- **Canva plugin**: The AI assistant plugins (ChatGPT plugin, Claude connector, etc.) that connect to the Canva MCP
- **Remote MCP server**: https://mcp.canva.com/mcp (Canva-hosted)
- **Self-hosted MCP**: Can be run locally using mcp-remote npm package

## 2. Prerequisites

1. **Canva account** with design capabilities
2. **AI agent platform** that supports MCP integration (e.g., Cursor, Claude, custom agent framework)
3. **Developer access** to Canva (for creating the MCP app in Canva Developer Portal)

## 3. Step-by-Step Implementation Plan

### Step 1: Set Up MCP Server Configuration

**Option A: Remote MCP Server (Recommended)**
- Use Canva's hosted MCP server at `https://mcp.canva.com/mcp`
- Configure your AI agent to use this server URL
- No server maintenance required

**Option B: Self-hosted MCP Server**
- Install `mcp-remote` npm package
- Configure `mcp.json` with Canva MCP server URL and OAuth credentials
- Run locally or on a server

**Configuration Example (VS Code settings.json):**
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

### Step 2: Create Canva MCP App in Developer Portal

1. Go to [Canva Developer Portal](https://www.canva.com/developers/apps)
2. Create a new app
3. Enable Canva MCP in the app settings
4. Note the client ID and client secret for OAuth authentication

### Step 3: Authenticate Users

- When the agent first connects, it will prompt the user to:
  1. Sign in to Canva
  2. Authorize the AI agent to access their Canva account
  3. Grant permissions for the specific operations needed (design creation, editing, etc.)

### Step 4: List Available MCP Tools

After authentication, the agent should:
1. Call `search-designs` to see available tools
2. Verify the connection is working
3. List the available operations (design generation, editing, asset management, etc.)

### Step 5: Design Creation Workflow

**For new designs:**
1. Use `generate-design` tool with user's description
2. Optionally use `generate-design-structured` for more controlled layouts
3. The tool will return design candidates that the user can select

**For editing existing designs:**
1. Use `search-designs` to find existing designs
2. Use `start-editing-transaction` to begin editing
3. Perform edits via `perform-editing-operations`
4. Commit changes with `commit-editing-transaction`

### Step 6: Design Management

- **Asset management**: Use `upload-asset-from-url` to add images/logos
- **Folder organization**: Use `create-folder`, `list-folders`, `move-design-to-folder`
- **Brand management**: Use `search-brand-templates`, `list-brand-kits`, `create-design-from-brand-template`

### Step 7: Export and Share

- Use `export-design` to get final designs in desired formats (PDF, PNG, JPG, PPTX, MP4, etc.)
- Use `resize-design` to adapt designs for different channels

## 4. Key Considerations

1. **Authentication**: Each user must authenticate individually (OAuth)
2. **Permissions**: Operations are limited by user's Canva plan and permissions
3. **Rate limits**: Follow the documented rate limits for each tool
4. **Plan requirements**: Some features (like brand templates) require paid Canva plans
5. **Error handling**: Handle authentication failures, rate limits, and permission errors gracefully

## 5. Terminology

- **MCP**: Model Context Protocol - the standardized interface
- **Canva AI Connector**: The official name for the integration
- **Agent**: The AI assistant that uses the MCP
- **Tool**: A specific MCP operation (e.g., generate-design, search-designs)

## 6. Recommended Approach

Call this an **MCP server** or **Canva MCP connection** rather than a "plugin" since:
1. It's based on the standardized MCP protocol
2. It connects directly to the Canva MCP server
3. It's designed for programmatic agent access, not just end-user browser extensions

This is the most accurate and professional terminology based on Canva's documentation.

---

## What Canva MCP Enables

After reading the docs, here's what your agents can do via the MCP tools:

- **Design generation**: Create designs from text descriptions (`generate-design`) or from structured candidates (`create-design-from-candidate`)
- **Design editing**: Start editing transactions, perform operations, commit changes
- **Design discovery**: Search designs, pages, folders (`search-designs`, `get-design`, `get-design-pages`)
- **Asset management**: Upload assets (`upload-asset-from-url`), list assets (`get-assets`)
- **Brand management**: Access brand kits and templates (`list-brand-kits`, `search-brand-templates`, `create-design-from-brand-template`)
- **Export**: Get designs as PDF/PNG/JPG/PPTX/MP4 (`export-design`)
- **Resizing**: `resize-design` (requires Canva Pro+)

---

## Important Constraints (from Canva's docs)

1. **Authentication**: Each user must authenticate individually via OAuth — there's no shared login token. The user must sign in and authorize the agent.
2. **Plan requirements**: Core tools (generate, search, export, comments) work on all plans. Brand templates, resizing, autofill require **Canva Pro or above**.
3. **AI credits**: Some AI-powered actions use monthly Canva AI allowance.
4. **Rate limits**: e.g., `generate-design` = 20 req/min, `search-designs` = 100 req/min.
5. **Remote server URL**: `https://mcp.canva.com/mcp` (production)

---

## Step-by-Step Plan (Before We Start Creating)

### Step 1 — Connect the Agent to the Canva MCP Server
- Configure your AI agent's MCP client to point at `https://mcp.canva.com/mcp`
- If your agent supports direct MCP URL config, add it there
- If not, install `npx mcp-remote@latest` and use stdio transport with that URL

### Step 2 — Authenticate the User
- When the agent first connects, it will prompt the user to **sign in to Canva** and authorize the agent to access their account
- Each user needs to do this individually; there's no way to bypass OAuth with just credentials

### Step 3 — Verify the Connection
- List available MCP tools to confirm the connection is live
- Test with a read-only call like `search-designs` before attempting to create anything

### Step 4 — Design Creation Workflow
- User says "create a design" → agent calls `generate-design` with the description
- Optionally use `generate-design-structured` for more controlled layouts
- Or `create-design-from-candidate` if starting from a template
- Return the design link/preview to the user

### Step 5 — Export / Deliver
- Call `export-design` to get the final design in the user's preferred format
- Share the Canva design URL back to the user

---

## Immediate Next Steps

Would you like me to:

1. **Set up the MCP server configuration** in this workspace (create `.cursor/mcp.json`, `.vscode/mcp.json`, or a `mcp.json` config file)?
2. **Build a small example agent script** that connects to Canva MCP and attempts `generate-design`?
3. **Walk through the Canva Developer Portal setup** (creating an app, enabling MCP, getting OAuth credentials)?

Let me know which path you'd like to take, and I'll start creating the actual files.