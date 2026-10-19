# farenwide-site

The Farenwide website (www.farenwide.com): landing page, privacy policy,
data deletion instructions, terms and support. Served by Firebase Hosting
(project farenwide-app); Meta's crawler can't read GitHub Pages.

Edit the pages in `build.py`, then run `python3 build.py` to regenerate the
HTML.

To publish: `python3 build.py && firebase deploy --only hosting`.

## Design dictionary

Farenwide has a six-colour palette: the five brand swatch colours, plus plum,
which the app added for shows and performances (`AppColors` in the Farenwide
app). Each part of the app owns one of them. Use it for that part's dot,
label, tile banner and accents everywhere: story chapters, feature tiles, the
active story dot, and anything new.

| Section      | Token         | Colour | Hex       |
|--------------|---------------|--------|-----------|
| Plan         | `--plan`      | Sky    | `#539FC7` |
| Party        | `--party`     | Sand   | `#A89169` |
| Journal      | `--journal`   | Sage   | `#668D64` |
| Playback     | `--playback`  | Amber  | `#DE9B3C` |
| AI assistant | `--assistant` | Lime   | `#AECC2E` |
| Passport     | `--passport`  | Plum   | `#8A6FAE` |

Text on a section colour (e.g. a tile banner) is ink, bold and at least
19px: it passes contrast on all six, where white fails on amber and lime.
Body text is ink (`#1B2A38`) and secondary text muted (`#5B6B78`).

In CSS, set `--accent: var(--<section>)` on a component and style it with
`var(--accent)`. In `build.py`, `SECTIONS` lists the sections in order; the
feature tiles are built from it and the story chapters name their section
from it, so add or rename a section there.

The page links `assets/site.css?v=<hash>`, so a deploy reaches visitors
straight away rather than after their cached stylesheet expires.
