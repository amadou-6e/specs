# Published-path compatibility: monitoring

This fixed compatibility container preserves original paths referenced by
published issues, pull requests, or other consumers. It is not an authoring
category for new entries and owns no contract or evidence body. Canonical
destinations are listed in the [migration map](../implementation/spec-migration.md).

| Element | Cardinality |
| --- | --- |
| README.md | 1 |
| `run-traces.md` | 1 |

The listed files are the closed pointer set. Do not copy a template or add new
specifications here. Each pointer is `superseded` and links its canonical owner.
Retain these paths while published references depend on them; removal requires
a consumer audit and an explicitly reviewed compatibility disposition.
