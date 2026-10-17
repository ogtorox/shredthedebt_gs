# Codebase map — shredthedebt_gs

| Path | Kind | Purpose |
|---|---|---|
| `main.py` | file | Streamlit dashboard entrypoint: page config + CSS, fetches the public Google Sheets CSV, renders metrics, chart, data table, and the self-report form |
| `src/` | dir | App modules (namespace package; `_init_.py` is empty and misspelled but harmless) |
| `src/chart_generator.py` | file | `generate_chart(df)` — horizontal bar chart of donations by company with headshot images fetched from raw.githubusercontent.com |
| `src/self_report.py` | file | `render_donation_form()` — Streamlit form for self-reporting a donation (shows a confirmation; no backend write) |
| `src/resize_logos.py` | file | Utility that generated the resized PNGs in `resized_logos/` |
| `src/app.py` | file | Empty placeholder (0 bytes) |
| `tests/` | dir | `conftest.py` and `test_chart_generator.py` are empty stubs — pytest collects 0 tests |
| `resized_logos/` | dir | Resized team-headshot PNGs (static assets) |
| `shredthedebt_gs/head_pngs/` | dir | Original headshot PNGs; served to the chart via raw.githubusercontent.com URLs |
| `.devcontainer/devcontainer.json` | file | Codespace config: Python 3.11 image, pip install of requirements, forwards port 8501 |
| `requirements.txt` | file | Fully pinned Python dependencies (Streamlit 1.42.2, pandas 2.2.3, matplotlib 3.9.4, …) |
| `README.md` | file | One-paragraph project description |
