---
name: agent-name
description: Use <when / trigger condition> to <outcome>. Write this as a delegation trigger — Claude reads it to decide when to hand work to this agent.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are <role>. Your job is to <outcome> for <who/what>.

## How you work

1. <first step and why>
2. <second step>
3. <verification step — how you know you are done>

## Boundaries

- <what you must not do, and why>
- <when to stop and report back instead of continuing>

## Output

Return to the caller:
- <what the final message contains, in what format>
