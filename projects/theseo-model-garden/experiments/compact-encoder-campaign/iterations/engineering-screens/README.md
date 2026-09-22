# Engineering screens

Role: prerequisite controls and learnability screens
Status: complete
Predecessor: none

This iteration groups smoke, classification-control, learnability, and dense-output
screens while preserving their separate inherited protocols. They are sequential
diagnostics, not repeated measurements: each later screen was authorized to isolate a
failure exposed by its predecessor.

Authorized sequence: deterministic smoke replacement -> frozen-representation probe
controls -> tiny-corpus query-decoder overfit -> direct dense-output positive control.

- [Execution](execution.md)
- [Results](results.md)
- [Evidence](evidence/README.md)
