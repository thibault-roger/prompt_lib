---
title: Write tests
description: Behavior-focused tests for a unit of code, including edge cases, in the project's existing style.
tags: [coding, testing]
variables: [framework, code, example_test]
version: 1.0.0
tested_with: [claude-opus-5-5, claude-sonnet-5-5]
---

## Prompt

Write tests for the code below using {{framework}}. The tests will live in an existing suite, so match the style of the example test: naming, fixtures, assertion style, file layout.

<code>
{{code}}
</code>

<example_test>
{{example_test}}
</example_test>

Test behavior, not implementation: a test should fail when the code does the wrong thing and keep passing through a refactor that preserves behavior. That means asserting on outputs and observable side effects, and mocking only at real boundaries (network, clock, filesystem, randomness).

Cover, in this order:
1. The main happy path(s).
2. Boundaries: empty input, single element, maximum sizes, zero/negative numbers, unicode, None/null.
3. Error paths: invalid input should raise the documented error, with the documented message if one exists.
4. Any branch in the code that the above does not reach.

Before the code, list the cases you will cover as a short bullet list so gaps are easy to spot. Give each test a name that states the expected behavior (`test_returns_empty_list_when_no_rows_match`). If the code has a bug that a test exposes, write the test to assert the *correct* behavior and flag the bug separately below the code.

## Notes

- **Use when:** adding tests for new or legacy code.
- If you have no existing tests, set `example_test` to "none — use the framework's idiomatic style".
- For data code (Polars/pandas), ask for small inline frames built in the test rather than fixture files; they make failures readable.

## Changelog

- 1.0.0 — initial version
