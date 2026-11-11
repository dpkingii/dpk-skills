---
name: spec
description: Interview the user about a feature or project, then write a spec they can build from. Use when the user wants to plan, scope or spec something before coding, or runs /spec with an idea.
allowed-tools: Read, Grep, Glob, Bash, AskUserQuestion, Write
---

# Spec interview

Turn a rough idea into a spec by asking only the questions the code and context can't answer.

## 1. Learn what already exists

Before asking anything, read the request and look at the project: README, CLAUDE.md, the code the idea touches, and any existing `.plans/` files. Note what is already decided, such as the stack, patterns, naming and data model. Never ask something you can find out by reading.

## 2. List what the spec must cover

Pick the areas that apply to this idea and drop the rest:

- Goal and who it is for
- Scope and non-goals
- Interfaces (UI, API, CLI, file formats)
- Data and state
- Failure and edge cases
- Security and privacy
- Performance limits
- Testing and success criteria
- Rollout and migration

## 3. Interview in rounds

Each round is one AskUserQuestion call with up to 4 questions about the open areas that matter most.

- Ask only when the answer changes what gets built. If a choice has a conventional default, use it and record it under Assumptions instead of asking.
- Give 2 to 4 concrete options. Put your recommendation first, mark it "(Recommended)" and say why in its description.
- Use previews to compare layouts, API shapes or schemas.
- Follow up when an answer opens new questions. Push back when an answer conflicts with an earlier one or with the code.
- After each round, give a one-line status of what is settled and what is left.

Stop when every area is decided, deferred or out of scope, or when the user says to stop. Don't add rounds just to be thorough.

## 4. Write the spec

Save it to `<cwd>/.plans/<slug>-spec.md`, where `<slug>` is a short kebab-case name for the topic. Use the absolute path. Don't save specs under `~/.claude/`.

```markdown
# <Title>

## Goal
## Non-goals
## Context
What exists today, with file paths.
## Decisions
Each decision, why it was made, and whether the user chose it or it is a default.
## Design
Interfaces, data and flow.
## Edge cases and failure handling
## Verification
Testable success criteria. For multi-step work, list each step with how to check it.
## Open questions
## Assumptions
```

Write in plain, direct sentences. Leave out sections that don't apply.

Reply with the path and any open questions. Don't repeat the spec in chat.

<instructions>$ARGUMENTS</instructions>
