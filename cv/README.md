# CV generator

Generates `kasun-hapangama.pdf` at the repo root, the file linked from the
site's "Resume (PDF)" buttons in `index.html`.

## Update the CV

1. Edit the `TEMPLATE` content in `generate_cv.py` (experience, projects, dates, links, etc).
2. Run:
   ```bash
   python3 cv/generate_cv.py
   ```
3. Commit the regenerated `kasun-hapangama.pdf` along with your `generate_cv.py` change.

## Format

Plain, standard ATS-format CV: Arial, black on white, single column, no
decorative layout. Only the header photo and the two certification badge
images are pulled in, straight from `assets/web/avatar.jpg` and
`assets/web/badges/`, so they stay in sync with what the site itself uses.

This is the only résumé format for this project, don't reintroduce a
separate visually-designed version.

## Requirements

- Python 3 (stdlib only, no pip installs).
- Google Chrome or Chromium installed locally, used headless for the
  HTML-to-PDF print step.
