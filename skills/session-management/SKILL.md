---
name: session-management
description: List, resume, fork, export, and import OpenCode v2 sessions from the CLI
---

# Session Management

OpenCode keeps persistent sessions you can resume, fork, export, or import.

## When to use

- You want to pick up where you left off
- You want to explore a different approach without losing the original
- You need to hand a session to a teammate

## Commands

```bash
# List sessions in the current project
opencode session list
opencode session list -n 10           # the 10 most recent
opencode session list --format json   # JSON instead of a table

# Resume the last session
opencode -c

# Resume a specific session
opencode -s <sessionID>

# Fork before changing direction (keeps the original intact)
opencode -c --fork
opencode run -s <sessionID> --fork "try a different approach"

# Export a session as JSON, redacting sensitive data
opencode session export <sessionID> --sanitize

# Import from a file or a share URL
opencode session import session.json
opencode session import https://opncd.ai/s/abc123

# Delete a session and its children
opencode session delete <sessionID>
```

## In the TUI

`/sessions` lists and switches sessions (aliases: `/resume`, `/continue`). `/fork` forks the current session. `/export` writes the conversation to Markdown.

## Notes

- v2 moved `export` and `import` under `opencode session`. The old top-level commands no longer exist.
- See https://opencode.ai/v2/docs/cli/
