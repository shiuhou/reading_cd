# Paper research in this repository

For a paper-reading task, select the relevant skill in `.agents/skills/` from the user's goal. The user can describe the task in ordinary language; they do not need to name a skill.

- Recent paper discovery or daily recommendations: `start-my-day`.
- Conference papers by venue and year: `conf-papers`.
- Read, explain, or critique a specific paper: `paper-analyze`.
- Retrieve figures from an arXiv paper or PDF: `extract-paper-images`.
- Search existing local paper notes: `paper-search`.

Read only the skills relevant to the task. Combine them when the request spans discovery, analysis, and note-taking. A general question about this repository does not need a paper workflow.

Use the user's research interests and requested output location. `config.example.yaml`, `config.yaml`, and `conf-papers/conf-papers.yaml` contain example interests and defaults; do not assume they describe the user. If the research config or Obsidian vault is unknown, give a useful answer in chat and ask for the missing path only when needed to search with that config or write notes. Treat heuristic scores as screening signals, and distinguish an abstract-based summary from a full-paper analysis.

The local skills use the current Codex model. The separate `web/` app has its own instructions in `web/AGENTS.md`.
