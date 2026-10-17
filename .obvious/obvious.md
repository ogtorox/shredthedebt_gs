# obvious.md — shredthedebt_gs

Agent guidance for **ogtorox/shredthedebt_gs** — a Streamlit dashboard tracking the
"Shred the Debt" charitable donation campaign (Chicago Global Shapers): live totals
per company, a donation bar chart with team headshots, and a self-report form.

## Stack

- **Runtime:** Python 3 (developed against 3.11 per devcontainer; verified on 3.13)
- **Framework:** Streamlit 1.42.2 + pandas + matplotlib + altair
- **Package manager:** pip, fully pinned in `requirements.txt`
- **Infra:** none — no database, no queue. Data comes from a public Google Sheets
  CSV; chart headshots are fetched from raw.githubusercontent.com. No secrets
  required to run locally (google-auth packages in requirements are unused by code).

## Commands

Run from the repo root. A ready virtualenv lives at `.venv/` in the sandbox snapshot.

```bash
# Install
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# Run (dev) — serves on http://localhost:8501
.venv/bin/streamlit run main.py --server.headless true

# Syntax check / tests
.venv/bin/python -m py_compile main.py src/*.py
.venv/bin/python -m pytest          # collects 0 tests today (test files are empty stubs)
```

No linter or typechecker is configured. No lock files to clean before starting.

## Codebase map

See `.obvious/codebase-map.md` for the full table. In short:

- `main.py` — dashboard entrypoint (the only thing to run)
- `src/chart_generator.py` — matplotlib chart, headshot overlays
- `src/self_report.py` — self-report donation form
- `src/resize_logos.py`, `resized_logos/`, `shredthedebt_gs/head_pngs/` — logo/image assets and the utility that generated them
- `tests/` — empty stubs; `src/app.py` — empty placeholder

## Local verification (from onboarding, 2026-10-17)

1. `streamlit run main.py` → parse port from output (8501).
2. `curl localhost:8501/_stcore/health` → `ok`; `GET /` → 200.
3. Primary flow in headless Chromium (Playwright): Total Donations metric,
   `$4,918.90` value, `Goal: $15,000` label, DONATE HERE button, chart SVG,
   data table, self-report form all render; zero console errors.
4. Headless data check: Google Sheets CSV returns 42 rows; `generate_chart(df)`
   returns a matplotlib Figure.

## Known quirks

- `main.py` originally called `render_donation_form()` without importing it —
  every page load crashed the self-report form with a NameError. Fixed in the
  onboarding PR by adding `from src.self_report import render_donation_form`.
- The devcontainer's `postAttachCommand` runs `src/chart_generator.py` as the app,
  which renders nothing (it is a module, not a page). The real entrypoint is `main.py`.
- `src/_init_.py` is a misspelled dunder; imports work regardless (namespace packages).
- README.md is a single paragraph; devcontainer.json is the real setup doc.

## Sandbox snapshot

- Snapshot ID: `nfqmh1xtttw21vq2xz98:default` (captured 2026-10-17T16:18:42Z)
- State: deps installed in `.venv/`, Streamlit running on 8501 under tmux session `dev`,
  Chromium available for Playwright checks. `main.py` fix present as an uncommitted
  change at capture time.
