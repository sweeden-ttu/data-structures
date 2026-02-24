# LaTeX Volumes: IEEE 752 Z-Field, PMBOK, and Blooming Directed Graph Tries

This directory contains the LaTeX source for the **IEEE 752 Z-Field Theory, Implementation and Specification Guidelines** and for **using PMBOK** to work with **Blooming Directed Graph Tries** and **anchor root Tries of Blooming Directed Graphs with filter agents and trigger processes** build.

## Structure

- **main.tex** — Main document; two parts (volumes) and five chapters.
- **chapters/**
  - **ieee752-zfield-theory.tex** — Volume 1: IEEE 752 Z-field theory (scope, definitions, integer rules, language mapping).
  - **ieee752-spec-guidelines.tex** — Volume 1: Implementation and specification guidelines (schema compliance, checklist).
  - **pmbok-integration.tex** — Volume 2: PMBOK integration (integration management, scope/WBS, quality, risk).
  - **blooming-directed-graph-tries.tex** — Volume 2: Blooming directed graph Tries (graph structure, Tries over graphs, cross-repo consistency).
  - **anchor-root-tries-filter-trigger.tex** — Volume 2: Anchor root Tries with filter agents and trigger processes (root anchor, filter agents, trigger process agent, build and PMBOK).

## Build

From this directory:

```bash
pdflatex main.tex
pdflatex main.tex
```

Or use your preferred LaTeX editor/IDE. Requires a standard LaTeX distribution (e.g. TeX Live, MacTeX) with `book`, `amsmath`, `hyperref`, `booktabs`.

## References

- `../IEEE_752_64BIT_GEOMETRICA_Z_FIELD_ZED_SPECIFICATIONS.md`
- `../BLOOMING_DIRECTED_GRAPH_AGENTS.md`
- `../TRIE_ROOT_ANCHOR.md`
