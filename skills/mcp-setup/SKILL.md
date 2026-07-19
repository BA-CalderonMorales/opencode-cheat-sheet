---
name: mcp-setup
description: Add and configure MCP servers in OpenCode, local or remote, including OAuth auth
---

# MCP Setup

MCP (Model Context Protocol) adds external tools alongside OpenCode's built-ins.

## When to use

- You need GitHub, Context7, Sentry, or a custom tool exposed to the agent
- You want to wire up OAuth for a remote server

## Steps

1. Add a server (interactive):
   ```bash
   opencode mcp add
   ```
2. List status:
   ```bash
   opencode mcp list
   ```
3. Authenticate an OAuth-enabled remote server:
   ```bash
   opencode mcp auth <name>
   ```

## Example config (remote, Context7)

```jsonc
{
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp",
      "headers": { "CONTEXT7_API_KEY": "{env:CONTEXT7_API_KEY}" }
    }
  }
}
```

Tip: MCP servers add to context — be selective. Disable with `"enabled": false`.
See https://opencode.ai/docs/mcp-servers/
