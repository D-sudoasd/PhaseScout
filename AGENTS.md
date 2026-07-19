# AGENTS.md — PhaseScout

Local **Materials Project** phase-scout toolkit: GUI + CLI + **project agent skill**.  
**Language:** Chinese notes OK; paths and `mp-xxxx` IDs exact.

## 1. What this is

| Item | Value |
|------|--------|
| Product | **PhaseScout** |
| GUI | `run_gui.bat` → `app.py` + `mp_client.py` |
| CLI | `scripts/fetch_possible_phases.py` |
| Parse | `composition_parse.py` |
| Elasticity web fallback | `elasticity_web.py` |
| Project skill | `.grok/skills/mp-possible-phases/` (`/mp-possible-phases`) |
| Runtime data | `downloads/0N_*/` (gitignored content) |
| Secrets | `config/settings.json` or `MP_API_KEY` — **never commit or print** |
| Not CURRENT | `__pycache__/`, empty shells, historical agent temps |

## 2. Read order

1. `README.md`
2. **Agent batch SOP** → `.grok/skills/mp-possible-phases/SKILL.md`
3. API / export → `mp_client.py`; GUI → `app.py`
4. Composition parse → `composition_parse.py`; batch CLI → `scripts/fetch_possible_phases.py`
5. CLI flags → `docs/CLI.md`

## 3. Agent batch download

When the user pastes an alloy/composition (or asks for 可能相 / CIF / Cij), **follow the project skill** and call the CLI only (do not improvise raw mp-api one-offs).

```powershell
# From repo root (portable; no machine-specific path required)
py -3.12 scripts\fetch_possible_phases.py "<composition>" --mode possible_phases --label <Label> --yes

# Near-stable + Cij (recommended when moduli matter)
py -3.12 scripts\fetch_possible_phases.py "<composition>" --mode near_stable --e-hull-max 0.05 --elasticity --label <Label> --yes
```

| Intent | Flags |
|--------|--------|
| Broad phase library | `possible_phases` |
| Near-stable / XRD seeds | `near_stable --e-hull-max 0.05` |
| Cij / 弹性 | `--elasticity` (web literature pack on MP miss) |
| Preview | `--dry-run` first if 4+ elements or unsure |

Prefer `--dry-run` first for large systems. Never echo API keys.  
CIF names: scheme B (`mp-id_formula_sg…`). Do not rename leaf CIFs after download.

## 4. Layout rules

- Default download root: `downloads/` (`DEFAULT_DOWNLOAD_DIR` in `app.py`).
- Batch folders: `0N_ascii_description`; do not rename leaf CIF names.
- Keep `run_gui.bat` and entry modules at repo root.
- Tests: `tests/`.
- Ship the project skill under `.grok/skills/` with the repo.

## 5. Do not

- Commit `config/settings.json` or put keys in docs/issues
- Treat MP DFT structures as experimental CIFs without checking
- Treat `elasticity_web_*` hits as verified numerical Cij (literature hints only; see `Cij_PROVENANCE.txt` / JSON `provenance`)
- Delete cross-batch “duplicate” `mp-id` files without proof + user OK
- Publish personal `downloads/` libraries to git
