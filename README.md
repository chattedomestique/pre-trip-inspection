# pre-trip-inspection

The Forest Hills Public Schools bus pre-trip inspection sheet (current as of 7/22/2026), as plain text and as a phone app for studying it.

- `pre-trip-inspection.md` is the full 17-page sheet as plain text, typos fixed.
- `pre-trip-inspection.html` is the app. It is one self-contained file: open it in any browser. Pick a section, step through the lines, and the part of the bus being checked lights up while the chin at the bottom shows exactly what to say.

## Sources

Edit these, then run `python3 build.py` to rebuild `pre-trip-inspection.html`.

- `src/content.txt` has every section and line, word for word. The header of each section names its diagram and the label above the text (say, point, do, indicate, tell, note). Each line lists the diagram parts it lights up, as `p=part,part`.
- `src/diagrams.py` and `src/diagrams.css` draw the 17 diagrams. Each part is a named group, and `content.txt` refers to those names.
- `src/app.js` and `src/page.css` are the app's behavior and layout.
- `vendor/styleguide/` is the small slice of the [styleguide](https://github.com/chattedomestique/styleguide) the page uses (branch `claude/generic-style-guide`), copied as built.

`build.py` stops with a list if a line names a part that its diagram does not have.

Diagram positions are a typical conventional school bus. Check them against your bus.
