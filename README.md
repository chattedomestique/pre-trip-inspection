# pre-trip-inspection

The Forest Hills Public Schools bus pre-trip inspection sheet (current as of 7/22/2026), as plain text and as a phone app for studying it.

- `pre-trip-inspection.md` is the full 17-page sheet as plain text, typos fixed.
- `pre-trip-inspection.html` is the app as one self-contained file: open it in any browser. Pick a section, step through the lines, and the part of the bus being checked lights up while the chin at the bottom shows exactly what to say.
- `docs/` is the same app as an installable PWA: it works offline, remembers which lines you have said, and the phone's back button leaves a section instead of the app.

## Install it on your phone

1. Turn on GitHub Pages: Settings, Pages, deploy from the `main` branch and the `/docs` folder. The app is then at `https://chattedomestique.github.io/pre-trip-inspection/`.
2. Open that address on your phone. On Android (Chrome) tap Install on the first screen, or the browser menu, then Install app. On iPhone (Safari) tap Share, then Add to Home Screen.
3. Open it once with a connection. After that it works with no signal at all.

Progress is saved on the device. When a new version is published, a notice at the top says so, and Reload swaps it in.

## Sources

Edit these, then run `python3 build.py` to rebuild `pre-trip-inspection.html` and `docs/`.

- `src/content.txt` has every section and line, word for word. The header of each section names its diagram and the label above the text (say, point, do, indicate, tell, note). Each line lists the diagram parts it lights up, as `p=part,part`.
- `src/diagrams.py` and `src/diagrams.css` draw the 17 diagrams. Each part is a named group, and `content.txt` refers to those names.
- `src/app.js` and `src/page.css` are the app's behavior and layout.
- `src/pwa.js`, `src/pwa.css`, `src/sw.js` and `src/manifest.webmanifest` make the installed app: the install button, the update notice, the offline worker and the manifest. `build.py` stamps the worker with a hash of the app, so every change installs as a new version.
- `src/mark.svg` is the icon. `python3 tools/make_icons.py` exports the five sizes into `docs/icons/`.
- `vendor/styleguide/` is the small slice of the [styleguide](https://github.com/chattedomestique/styleguide) the page uses (branch `claude/generic-style-guide`), copied as built.

`build.py` stops with a list if a line names a part that its diagram does not have.

Diagram positions are a typical conventional school bus. Check them against your bus.
