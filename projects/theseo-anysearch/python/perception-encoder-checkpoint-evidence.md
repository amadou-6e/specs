# Checkpoint diagnostic evidence

Issues specs#37 / theseo-anysearch#362. Protocol frozen at
`df765d0d4eed2f74a1d6e85f358e435e126d4b08`, executable `d7b8e7a`.

Completed all three trajectories and the frozen probe ladder. Every seed selected
update 256 from the same 2048-update trajectory. Recorded elapsed time 71.39s.
Zero encoder updates. No promotion or changes to previous verdicts.

Selected reference F1: 0.3829/0.3990/0.4017; final: 0.3676/0.3736/0.3865;
frozen probe: 0.6006/0.5847/0.5699. Selected loss improves over final by 0.2529
(paired 95% CI [0.2339,0.2725]), but exceeds probe loss by 0.1495
(paired improvement interval [-0.1639,-0.1353]).

Outcome `reference_improves_below_probe`: refine the reference before attributing
encoder failure. Earlier checkpoints and regularization/data coverage are possible
new interventions, not tested conclusions or adopted protocol modifications.

Implementation report: `docs/perception-encoder-checkpoint-assessment.md` on exp/362.
Machine-readable payload SHA256:
`72f39596cef5d24bf12ab2469c9950c1e7bab6411ea93436e97be58f9cee7f42`.
Only compact evidence is committed; model/prediction artifacts remain untracked.
