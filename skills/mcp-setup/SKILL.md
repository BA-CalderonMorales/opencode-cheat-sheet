---
name: mcp-setup
description: Add and configure MCP servers in OpenCode v2, local or remote, including OAuth auth
---

# MCP Setup

MCP (Model Context Protocol) adds external tools alongside OpenCode's built-ins.

## When to use

- You need GitHub, Context7, Sentry, or a custom tool exposed to the agent
- You want to wire up OAuth for a remote server

## Steps

1. Add a server:
   ```bash
   # Remote (HTTP)
   opencode mcp add context7 --url https://mcp.context7.com/mcp

   # Local (stdio)
   opencode mcp add everything -- npx -y @modelcontextprotocol/server-everything

   # Add it to the global config instead of this project
   opencode mcp add context7 --global --url https://mcp.context7.com/mcp
   ```
2. Check the connection status:
   ```bash
   opencode mcp list
   ```
3. Authenticate an OAuth-enabled remote server:
   ```bash
   opencode mcp auth sentry
   opencode mcp auth        # pick from the OAuth-capable servers
   ```
4. Drop stored credentials when you need to re-sign-in:
   ```bash
   opencode mcp logout sentry
   ```

## Config format

Servers live under `mcp.servers` in v2, and the on/off flag is `disabled`:

```jsonc
{
  "mcp": {
    "servers": {
      "context7": {
        "type": "remote",
        "url": "https://mcp.context7.com/mcp",
        "headers": { "CONTEXT7_API_KEY": "{env:CONTEXT7_API_KEY}" }
      },
      "everything": {
        "type": "local",
        "command": ["npx", "-y", "@modelcontextprotocol/server-everything"],
        "cwd": "."
      }
    }
  }
}
```

Remote servers use OAuth by default. Set `"oauth": false` when the server only takes an API key or a static header.

## Removing a server

Delete its entry from the config file where it was added. There is no `mcp remove` command.

## Tips

- MCP servers eat context. Keep the list short.
- `/mcps` in the TUI shows the same status as `opencode mcp list`, and lets you connect, disconnect, or authenticate.
- See https://opencode.ai/v2/docs/mcp-servers/
