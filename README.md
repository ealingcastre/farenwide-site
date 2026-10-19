# farenwide-site

The Farenwide website (www.farenwide.com): landing page, privacy policy,
data deletion instructions, terms and support. Served by Firebase Hosting
(project farenwide-app); Meta's crawler can't read GitHub Pages.

Edit the pages in `build.py`, then run `python3 build.py` to regenerate the
HTML.

To publish: `python3 build.py && firebase deploy --only hosting`.

## Design dictionary

Each part of the app has one colour. Use it for that part's dot, label and
accents everywhere: story chapters, feature cards, the active story dot, and
anything new. The colours are the app's own (`AppColors` in the Farenwide app).

| Section  | Token        | Colour  | Hex       |
|----------|--------------|---------|-----------|
| Plan     | `--plan`     | Sky     | `#539FC7` |
| Party    | `--party`    | Sand    | `#A89169` |
| Journal  | `--journal`  | Sage    | `#668D64` |
| Playback | `--playback` | Amber   | `#DE9B3C` |
| Passport | `--passport` | Plum    | `#8A6FAE` |

In CSS, set `--accent: var(--<section>)` on a component and style it with
`var(--accent)`. In `build.py`, `SECTIONS` lists the sections in story order;
the story chapters and feature cards are both built from it, so add or rename
a section there.

Text is ink (`#1B2A38`) and secondary text muted (`#5B6B78`).
