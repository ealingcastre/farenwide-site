# farenwide-site

The Farenwide website (www.farenwide.com): landing page, privacy policy,
data deletion instructions, terms and support. Served by Firebase Hosting
(project farenwide-app); Meta's crawler can't read GitHub Pages.

Edit the pages in `build.py`, then run `python3 build.py` to regenerate the
HTML.

To publish: `python3 build.py && firebase deploy --only hosting`.
