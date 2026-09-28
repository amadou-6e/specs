# Current AGENTVIZ UI reference

Open [agentviz-current-ui.drawio](agentviz-current-ui.drawio) in diagrams.net. Its ten pages pair a locked source screenshot on the left with an editable reconstruction on the right. The reconstruction uses separate rectangles, labels, controls, cards, bars, and panels so layout and styling can be changed directly in Draw.io.

The pages cover Find, Review, Investigate, Analyze Stats, Analyze Tracks, Analyze Waterfall, Analyze Graph, Analyze Cost, Compare, and Improve at a 1400 × 860 desktop viewport. They show one demo-session state per page, not every interaction state or compact layout. The Compare page shows the empty comparison state, since the demo provides only one session.

The [references](references/) directory holds the screenshots used for fidelity comparison. Seven were copied from AGENTVIZ's documented demo captures at source commit `9f32319e8d6c44fbbfcec06eadb1dda38f569c6d`. Review, Compare, and Cost were captured from the running AGENTVIZ demo at the same viewport on 2026-09-27. The older `docs/screenshots/cost-view.png` was omitted because it shows an obsolete shell.

This is a current-state reference study. For new Laomedo behavior, create view-owned Draw.io specifications under `projects/laomedo/views/<view>/ui/`. Do not treat the reference screenshot or this index as a specification for interactions absent from the editable geometry.
