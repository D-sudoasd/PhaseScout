# PhaseScout agent workflow (detail)

## 1. Intake

From free text extract:

- Composition / grade / chemsys (`Ti-6Al-4V`, `Ti-Al-V`, `Ti 90 Al 6 V 4 wt%`, aliases like TC4)
- Optional batch label
- Optional explicit `mp-####` list
- Intent flags: dry-run only? near-stable? Cij? offline?

If composition is ambiguous (e.g. “Ti65” multi-element family), state assumed elements and offer to correct before a large download.

## 2. Mode selection examples

| User says | Action |
|-----------|--------|
| “所有可能相 / 建相库” | `possible_phases` |
| “稳态附近 / 给 MAUD 种子” | `near_stable --e-hull-max 0.05` |
| “带弹性常数 / Cij” | add `--elasticity` |
| “先别下，看看有多少” | `--dry-run` |
| “就这三个 mp-id” | `mpids_only` |

## 3. Size gates

| Situation | Behavior |
|-----------|----------|
| ≥4 elements, user did not insist on full download | dry-run first |
| Unique candidates > 200 | require explicit yes / `--yes` |
| User already said 下载/全部/yes | may pass `--yes` |

## 4. Execution order

```text
dry-run (optional)
  → show subsystem_counts + unique_n
  → user confirm if large
download (± --elasticity)
  → report paths
if elasticity and web_hints
  → point to elasticity_web_search.csv / web_hits.jsonl
  → do not claim numerical Cij for those rows
CIF2Peaks CLI on the same batch folder
  → <batch>/cif2peaks_complete.xlsx
  → do not open the GUI; do not invent missing Cij
```

## 5. Failure handling

| Symptom | Fix |
|---------|-----|
| No API key | Point to `config/settings.example.json` / `MP_API_KEY`; never invent key |
| `mp-api` missing | `pip install -r requirements.txt` |
| Many CIF ok but elasticity missing | Expected; explain MP coverage + web pack |
| OpenAlex timeouts | Re-run with `--elasticity-web-offline` or `--no-elasticity-web` |
| Path not found | Ensure cwd is repo root |

## 6. What not to do

- Hand-written loops over `MPRester` in the chat instead of CLI  
- Mixing JARVIS/AFLOW numbers into MP Cij columns without a separate source field  
- Rewriting historical `downloads/` libraries “to clean duplicates”
