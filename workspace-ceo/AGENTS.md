# Available Agents

## coder
- **Specialty**: Software engineering, script generation, filesystem ops, shell execution, git operations.
- **When to use**: Any request requiring code implementation, bug fixing, file manipulation, or command execution.
- **Spawn with**: `sessions_spawn` targeting agent `coder`.
- **Always set**: `deliver: false` so the coder replies to YOU, not the user.

## reviewer
- **Specialty**: Code review, security auditing, static analysis, anti-pattern detection.
- **When to use**: ALWAYS after coder returns a code payload, BEFORE returning results to the user.
- **Spawn with**: `sessions_spawn` targeting agent `reviewer`.
- **Always set**: `deliver: false` so the reviewer replies to YOU, not the user.
- **On REJECT**: Use `sessions_send` to pass reviewer feedback to the coder's existing session for fixes.
- **On APPROVE**: Instruct coder to commit and push to a feature branch, then report to user.
