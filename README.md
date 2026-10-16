# AI Retreat 2026: products

This private repository holds the products I build at the AI Retreat in Bad Kohlgrub (16 to 18 October 2026) from content the group shares.

## Reproducibility

The extracted data and the code are shared, and every number and figure in the slides can be reproduced. The code, the codebook and the build scripts are in this repository. The extracted datasets (CSV, no names) are shared with the group; place them in `shared/daten/` and run `quarto render` from the repository root to rebuild the slides in `docs/`.

## Structure

- `shared/` holds the shared material: transcripts, board content and files from others. It is listed in `.gitignore` and exists only on my laptop.
- `shared/transcripts/` holds the transcripts, mine and those of others. File names start with the date and the name of the person who recorded them, for example `2026-10-16-lars-03-sabine.md`.
- `products/` holds one folder per product.
- `log/` has one short entry per work session, named by date.

## What stays out of git

The shared material contains names and personal details of other people. It is never committed, because the history of a repository is permanent. Products are committed only when they contain no personal data, for example a summary of themes without names.

## Who

Lars Schöbitz. Work happens on `dev`.
