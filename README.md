# AI Retreat 2026: products

This repository holds the products I build at the AI Retreat in Bad Kohlgrub (16 to 18 October 2026) from content the group shares.

## Reproducibility

The extracted data and the code are shared, and every number and figure in the slides can be reproduced. The code, the codebook and the build scripts are in this repository. The extracted datasets (CSV, no names) are in `products/daten/`; sensitive statements keep their codes there, but their text is emptied. Run `quarto render` from the repository root to rebuild the slides in `docs/`.

## Structure

- `shared/` holds the shared material: transcripts, board content and files from others. It is listed in `.gitignore` and exists only on my laptop.
- `shared/transcripts/` holds the transcripts, mine and those of others. File names start with the date and the name of the person who recorded them, for example `2026-10-16-lars-03-sabine.md`.
- `products/` holds one folder per product.
- `log/` has one short entry per work session, named by date.

## What stays out of git

The shared material contains names and personal details of other people. It is never committed, because the history of a repository is permanent. Products are committed only when they contain no personal data, for example a summary of themes without names.

## Learnings

### 16 persons in the data, 15 at the hike

The slides counted 16 persons, but the group was 15. The count is the number of distinct speaker IDs (P01 to P16) in `speakers.csv`, and one person got two IDs.

- Speaker IDs were assigned from what people said about themselves, because most transcripts have no speaker labels and names are rarely said aloud.
- One person appears in two recordings (T10 and T20) with different descriptions of their work. Each recording got its own ID, P13 and P16. The local name key already flagged P16 as "possibly P13", but the build counted IDs, not people.
- The two IDs never occur in the same recording, which fits one person.

Next time: get the participant list before coding, settle uncertain IDs before any number goes on a slide, and let the build stop while the key still holds a "possibly" entry. A head count from outside the data is the check the data cannot give itself.

Fixed on 16 October 2026: P16 is merged into P13, so the IDs now run from P01 to P15 and the slides count 15 persons. `build.py` now stops when an ID used in the data is still marked as possibly another person.

## Who

Lars Schöbitz. Work happens on `dev`.
