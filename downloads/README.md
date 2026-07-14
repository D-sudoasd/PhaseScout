# downloads/ (runtime output)

PhaseScout writes CIF batches and indexes here (for example `01_my_alloy/`).

This directory is **gitignored** except this README and `.gitkeep`.  
Your local phase libraries stay on disk but are not published to GitHub.

Suggested layout after a CLI run:

```text
downloads/
  01_Ti6Al4V/
    phase_index.csv
    query_summary.txt
    run_manifest.json
    mp-xxxx_Formula.cif
```
