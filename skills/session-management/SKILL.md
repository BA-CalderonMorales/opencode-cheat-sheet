---
name: session-management
description: List, resume, fork, export, and import OpenCode sessions from the CLI
---

# Session Management

OpenCode keeps persistent sessions you can resume, fork, or share.

## When to use

- You want to pick up where you left off
- You want to explore a different approach without losing the original
- You need to hand a session to a teammate

## Commands

```bash
# List recent sessions
opencode session list -n 10

# Resume the last session
opencode -c

# Resume a specific session
opencode -s <sessionID>

# Fork before changing direction (keeps the original intact)
opencode -c --fork

# Export a session (redact secrets with --sanitize)
opencode export <sessionID> --sanitize

# Import from file or share URL
opencode import session.json
opencode import https://opncd.ai/s/abc123
```

In the TUI: `/sessions` to list/switch, `/share` to create a link, `/unshare` to remove it.
See https://opencode.ai/docs/cli/ and https://opencode.ai/docs/share/
