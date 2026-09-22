# Experiment iterations

This container holds the distinct planned or permitted iterations of one experiment.
All iterations answer the parent experiment's research questions under its governing
protocol; they do not silently redefine that protocol.

## Contained elements

```text
iterations/
â”œâ”€â”€ 1 README.md
â””â”€â”€ 1..* <iteration>/
```

Use stable ordered names such as `iteration-001`, `iteration-002`, and so on. An
iteration may represent the primary run, a permitted adaptation, a rerun, or a
replication. Its README must state its role, predecessor if any, applicable protocol
gate, and why another iteration was allowed.

Iterations are ordered records, not independent experiments. Create a new experiment
instead when the research question or governing protocol changes outside its declared
adaptation rules.
