# Edge style for the candidate ERD

This is the routing contract for `unified-income-expense-candidate.drawio`. It changes the presentation of proposed relationships, not the relationship definitions or cardinalities in `graph.yaml` or the candidate. Apply it when simplifying the diagram; review the exact exported result after every edit. The [editable visual examples](edge-style-examples.drawio) show each rule as a use/avoid comparison. Section 07 in the same file applies the port and trunk rules to the dense Account area marked in the candidate ERD.

## Visual language

| Link | Draw.io style | Meaning |
| --- | --- | --- |
| Structural or evidence relationship | Orthogonal, unrounded, solid `#3D607E`, width `1.8` | Ordinary object relationship. |
| Reimbursement cross-link | Orthogonal, unrounded, dashed `#B36C3E`, width `1.5` | Income associated with an Expense or Expense Item. |

Keep crow's-foot symbols at both ends with the actual optionality and multiplicity. Do not replace them with a generic arrow. A label states a condition only when needed, such as `if direction = income`; it does not substitute for cardinality. Color and dashing distinguish link roles, never confidence or approval state.

## Routing order

Apply these in order. Do not improve a lower-priority property by breaking a higher-priority one.

1. Preserve the intended source, target, port and cardinality. A line must visibly terminate at the correct card.
2. Do not cross a card, card text, cardinality marker, lane heading or edge label. A route may cross an empty lane area.
3. Minimize crossings between edges and keep adjacent endpoints distinguishable. Cross at a right angle when unavoidable; avoid long shared segments that look like a junction.
4. Use the shortest clear orthogonal route with the fewest bends. A direct parent-child link stays within its column. Cross-band links use a clear horizontal corridor between bands and a vertical approach to the destination.
5. Align related routes on shared channels and keep parallel lines evenly spaced. Do not add a bend solely to force visual symmetry.

## Geometry

- Use a 10-unit routing grid. Use at least 30 units between a routed segment and an unrelated card or lane heading, measured to the card border where space permits.
- Give consecutive parallel trunks and same-side attachment ports an even 20-unit pitch when the corridor is clear. A minimum 20-unit gap with uneven gaps across the sequence is not sufficient. If an obstacle forces a deviation, separate the affected route into another clear corridor; do not compress several lines into an indistinguishable bundle.
- Prefer the middle of a card side for a single connection. Spread multiple connections along that side in stable order, leaving at least 20 units between attachment points and room for the crow's-foot symbols.
- Parent-child pairs within one column attach bottom-to-top and run vertically. Side-to-side links between adjacent columns run horizontally unless an obstacle requires a short detour.
- For a distant target, use one vertical trunk near the source, one horizontal corridor, and one short destination approach where possible. Keep trunks outside unrelated cards. Do not route an edge through its own child card.
- Reserve the white gap between the top object columns and the Transactions and receipts band for top-to-evidence links. Reserve the gap between Transactions and receipts and the lower reporting band for evidence-to-reporting links. Keep unrelated routes out of those corridors when a shorter local path exists.
- Use no diagonal segments, rounded corners, arrowheads other than cardinality markers, or edge-to-edge junctions. Do not use an edge as a shared bus: every relationship remains individually traceable.

## Review before accepting a routed diagram

Check every edge at both endpoints and trace its entire path at readable zoom. Count card/label crossings, edge crossings and bends; resolve card/label crossings first, then reduce the other counts. Check the whole page for consistent spacing and local areas for overlapping symbols or ambiguous near-parallel lines. The validator checks object and endpoint identity but cannot prove these geometric conditions, so inspect an export of the exact final Draw.io file.

## Script-assisted crossing audit

Run `python tools/audit_drawio_edges.py projects/financial-workspace/exp-model/relationships/unified-income-expense-candidate.drawio` from the `specs` repository root before final visual review. It prints edge IDs and coordinates where two saved orthogonal waypoint segments cross. The previous Account–Budget and Account–Forecast crossing is covered by a regression test in `tools/test_audit_drawio_edges.py`.

Treat results as candidates to inspect and resolve, not an automatic pass/fail gate: some crossings are necessary, and Draw.io can route endpoint segments differently from the saved waypoints. The script deliberately omits those endpoint segments and cannot check card overlap, legibility, or rendered cardinality markers. Render the exact final file and trace every edge after running it. Record any crossings you retain and why they cannot be avoided.
