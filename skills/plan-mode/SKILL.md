---
name: plan-mode
description: Use OpenCode Plan agent and Tab switching to propose changes before editing
---

# Plan Mode

Separate thinking from doing: get a proposal, review it, then approve edits.

## When to use

- Non-trivial refactors or migrations
- Anything you'd want a junior dev to plan first
- Exploring an unfamiliar codebase before touching it

## Steps

1. Press **Tab** to switch to the **Plan** agent (read-only; `edit`/`bash` ask by default).
2. Describe the feature with context and examples:
   ```
   When a user deletes a note, flag it deleted in the DB, then build a screen
   listing recently deleted notes with undelete / permanent delete.
   ```
3. Review the plan and iterate.
4. Press **Tab** back to **Build**, then:
   ```
   Sounds good! Go ahead and make the changes.
   ```

## Config (optional)

Make Plan the default agent project-wide:

```jsonc
{ "default_agent": "plan" }
```

You can also scope a custom command to the plan agent — see https://opencode.ai/docs/commands/
See https://opencode.ai/docs/agents/
