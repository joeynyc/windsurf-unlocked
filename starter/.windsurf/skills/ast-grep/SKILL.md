---
name: ast-grep
description: Use ast-grep for structural (AST-aware) code search and refactoring instead of plain ripgrep when the intent depends on code structure — not just text matching. Triggers on refactors, codemods, "find all X that don't Y", or any search where naive grep would miss edge cases.
version: 1.0.0
trigger: >
  Any request that requires understanding code structure (not just text):
  - "Find all async functions without try/catch"
  - "Rewrite every useState<X>(y) to useSignal<X>(y)"
  - "Find React components using a specific hook"
  - "Find functions with >3 parameters"
  - "Replace console.log only inside class methods"
  - Any refactor spanning > 5 files
---

# ast-grep

Structural code search. You understand code's abstract syntax tree, not just its text.

## When to Use ast-grep vs ripgrep

| Task | Tool |
|------|------|
| Find a string literal | `rg` |
| Find a comment | `rg` |
| Find all exports | `rg` (fast enough) |
| Find all async functions that await outside try/catch | **`ast-grep`** |
| Refactor `foo(bar)` → `foo.method(bar)` everywhere | **`ast-grep`** |
| Rename a class across a TypeScript codebase | **`ast-grep`** (catches shorthand, destructuring, types) |
| Find components that receive a specific prop | **`ast-grep`** |

Default to `rg` for text; escalate to `ast-grep` when the pattern needs grammar awareness.

## Installation

```bash
brew install ast-grep          # macOS
cargo install ast-grep         # cross-platform
npm install -g @ast-grep/cli   # Node-friendly
```

Verify: `ast-grep --version` (should print a 0.x.x or later).

## Basic Usage

### Find pattern

```bash
# Find all console.log calls inside class methods
ast-grep --lang ts --pattern 'class $_ { $$ { console.log($$$) } $$ }'

# Find React components using useEffect with empty deps
ast-grep --lang tsx --pattern 'useEffect($_, [])'

# Find async functions without try/catch
ast-grep --lang ts --pattern 'async function $NAME($$) { $$ }' \
  | grep -v 'try {'
```

### Rewrite in place

```bash
# Convert var → let (demonstrative; use at your own risk)
ast-grep --lang js \
  --pattern 'var $NAME = $VAL' \
  --rewrite 'let $NAME = $VAL' \
  --update-all
```

### Rule files

For complex patterns, write a YAML rule in `.ast-grep/rules/`:

```yaml
# .ast-grep/rules/no-console-in-prod.yml
id: no-console-in-prod
language: typescript
rule:
  pattern: console.log($$$)
  not:
    inside:
      kind: if_statement
      has:
        pattern: process.env.NODE_ENV === 'development'
message: "console.log outside dev-mode guard"
severity: error
```

Run: `ast-grep scan`.

## Agent Protocol

When the user asks for a code search that depends on structure:

1. **Decide the right tool.** Is this pattern purely textual? Use `rg`. Does it depend on AST context (inside class, function, expression)? Use `ast-grep`.
2. **Write the pattern.** Use metavariables `$_` (wildcard), `$NAME` (named), `$$$` (multiple). Test on a single file first.
3. **Scope the search.** Always pass `--lang <lang>` and a path argument — not the whole repo if you can avoid it.
4. **Preview before rewriting.** Never pass `--update-all` without first running without it and reading the output.
5. **For refactors > 10 files**, write a rule file in `.ast-grep/rules/` and commit it. Reproducibility > one-off commands.

## Language Support

ast-grep ships first-class support for:
TypeScript, TSX, JavaScript, JSX, Python, Rust, Go, Java, Kotlin, Swift, C, C++, C#, Ruby, PHP, HTML, CSS, YAML, JSON, Bash.

If your language is missing, check the [ast-grep playground](https://ast-grep.github.io/playground.html) for tree-sitter grammar coverage.

## Common Patterns Cheat Sheet

| Intent | Pattern |
|--------|---------|
| Any function with > N args | `function $NAME($A, $B, $C, $D, $$$)` |
| React class component | `class $_ extends React.Component { $$ }` |
| Async function | `async function $_($$) { $$ }` |
| Arrow function | `($$) => $_` |
| Call with specific first arg | `$FN("specific-arg", $$)` |
| TypeScript generic call | `$FN<$T>($$)` |

## Never

- **Never** use ast-grep for plain string/text search — `rg` is 10x faster and the right tool
- **Never** run `--update-all` without first running the same pattern without it and reading the diff
- **Never** leave complex patterns as one-off commands — commit them as rule files in `.ast-grep/rules/`
- **Never** run against `node_modules/`, `vendor/`, `dist/`, or build output — always scope with a path argument
- **Never** trust a rewrite across a codebase without running the test suite after

## Credits

Reference from the [official ast-grep AI docs](https://ast-grep.github.io/advanced/prompting.html), prompting pattern originally from [Kieran Klaassen on X](https://x.com/kieranklaassen/status/1938453871086682232).
