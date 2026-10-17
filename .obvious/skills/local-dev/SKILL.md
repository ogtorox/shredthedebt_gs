---
name: local-dev
description: How to get the shredthedebt_gs Streamlit dashboard running locally, verified during onboarding (2026-10-17)
---

# local-dev — shredthedebt_gs

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt   # ~2 min on the sandbox, all wheels prebuilt
```

Python 3.11 (devcontainer image) is the target; 3.13 works identically — every
pinned dep ships 3.13 wheels. No Docker, no database, no env vars, no secrets.

## Run

```bash
.venv/bin/streamlit run main.py --server.headless true
```

- Port is printed in startup output — `http://localhost:8501`.
- Run from the repo root: `main.py` does `from src.chart_generator import …`.
- No lock files exist or are needed; kill leftovers with `pkill -f "streamlit run"`.

## Verify (what onboarding actually checked)

1. `curl localhost:8501/_stcore/health` → `ok`; `GET /` → 200.
2. Headless Chromium (Playwright is preinstalled in the snapshot): load `/`,
   wait ~12 s for the websocket render, then assert the page shows the
   Total Donations metric (`$4,918.90` live value), `Goal: $15,000`, DONATE HERE
   button, a chart `<svg>`, the dataframe, and the self-report form; console must
   be clean. Screenshots land at `/tmp/dashboard_top.png`, `/tmp/dashboard_table.png`.
3. Headless data check: `pd.read_csv` on the SHEET_CSV_URL in `main.py` → 42 rows;
   `generate_chart(df)` returns a Figure (hits raw.githubusercontent.com for headshots).

## Gotchas learned the hard way

- `main.py` shipped calling `render_donation_form()` without importing it — the
  form (last element) died with a NameError on every load while everything above
  it looked fine. Always assert the form text is present, not just the metrics.
- The devcontainer `postAttachCommand` runs `src/chart_generator.py`, which is a
  library module — it serves a blank page. The real entrypoint is `main.py`.
- `tests/` files are 0-byte stubs; pytest collects nothing. Don't mistake
  "no tests ran" for success or failure of app health.
- Data is a live public Google Sheet; totals change. Assert on structure
  (labels, elements), not exact values, except as smoke evidence.

## Validation summary at onboarding time

- dev_stack_healthy: true
- Runtime: Python 3.13 / Streamlit 1.42.2; deps pinned; venv at `.venv/`
- Primary flow: verified end-to-end in headless Chromium, zero console errors
- Tests: 0 collected; `py_compile` passes on all 4 source files; no linter configured
