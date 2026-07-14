# AGENTS.md — PhaseScout

Local **Materials Project** phase-scout toolkit: GUI + CLI + optional agent skill.  
**Language:** Chinese notes OK; paths and `mp-xxxx` IDs exact.

## 1. What this is

| Item | Value |
|------|--------|
| Product | **PhaseScout** |
| GUI | `run_gui.bat` → `app.py` + `mp_client.py` |
| CLI | `scripts/fetch_possible_phases.py` |
| Parse | `composition_parse.py` |
| Runtime data | `downloads/0N_*/` (gitignored content) |
| Secrets | `config/settings.json` or `MP_API_KEY` — **never commit or print** |
| Not CURRENT | `__pycache__/`, empty shells, historical agent temps |

## 2. Read order

1. `README.md`
2. API / export → `mp_client.py`; GUI → `app.py`
3. Composition parse → `composition_parse.py`; batch CLI → `scripts/fetch_possible_phases.py`
4. CLI flags → `docs/CLI.md`
5. User skill → `~/.grok/skills/mp-possible-phases/SKILL.md` (`/mp-possible-phases`)

## 3. Agent batch download

When the user pastes an alloy/composition, call the CLI (do not improvise raw mp-api one-offs):

```powershell
cd "D:\Backup\桌面\PhaseScout"
python scripts\fetch_possible_phases.py "<composition>" --mode possible_phases --label <Label> --yes
```

Prefer `--dry-run` first for large systems (4+ elements). Never echo API keys.

## 4. Layout rules

- Default download root: `downloads/` (`DEFAULT_DOWNLOAD_DIR` in `app.py`).
- Batch folders: `0N_ascii_description`; do not rename leaf CIF names.
- Keep `run_gui.bat` and entry modules at repo root.
- Tests: `tests/`.

## 5. Do not

- Commit `config/settings.json` or put keys in docs/issues
- Treat MP DFT structures as experimental CIFs without checking
- Delete cross-batch “duplicate” `mp-id` files without proof + user OK
- Publish personal `downloads/` libraries to git
