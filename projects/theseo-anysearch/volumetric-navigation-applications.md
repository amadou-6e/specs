# Volumetric Navigation Application Library

Status: proposed research program; no external assets acquired, adapters and experiments not implemented.
Owner: amadou-6e. Updated: 2026-09-13. Tracking: [specs#82](https://github.com/amadou-6e/specs/issues/82).

## Purpose And Boundaries

Build useful flying and swimming navigation in constrained 3D spaces, starting with
small local environments. The opportunity is to reduce manual waypoint placement,
route repair and navigation QA, not merely demonstrate another shortest-path solver.
This catalog defines applications and their experiments; it is not a frozen run
preregistration or evidence of deployment readiness.

Our compact frozen encoder is a candidate feature source, not a proven planner.
Its validated interface is a 729-number code from a 33-cubed local input, with
central 17-cubed geometry predictions through its native decoder. Collision-head
experiments did not beat raw-grid/spatial controls. Preserve these controls here.
Do not interpret local predictions as full-world topology or reliable hidden-space
collision certificates. Exact collision checks remain authoritative.

## Application Catalog

All rows below are proposed applications, not existing Theseo features. Priority
is implementation order, not a claim about commercial demand.

| ID / priority | Application and work removed | Training ground and controlled difficulty | Training requirements | Evaluation and additional work |
| --- | --- | --- | --- | --- |
| V01 / first | Indoor flying companion or inspection drone: replace hand-authored 3D waypoints through rooms, vents and hangars | Seeded rooms, columns, shafts and portals; vary radius-to-aperture ratio, turns, detour and vertical transitions independently | Start with full occupancy, spherical body and translation actions; A* expert paths, local successor ranking or imitation; frozen-code, spatial and raw observations | Collision-free arrival, stretch, clearance, p95 latency; implement conservative finite-body and swept-edge checks before claiming body-safe flight |
| V02 / second | Underwater cave or wreck navigation: avoid manually marking swim corridors and dead ends | Tube networks, chambers, wreck-like partitions; loops, bottlenecks, dead-end depth and restricted water volumes | Reuse static V01 geometry only for the initial holonomic swimming proxy; add water mask, velocity, turn-rate, buoyancy/current only in separate tasks | Arrival without leaving water, minimum clearance and control feasibility; geometry-only results are not hydrodynamic results |
| V03 / second | Forest/canyon aerial pursuit: reduce bespoke escape routes around branches and overhangs | Vertical trunks plus branching clutter, arches and ravines; obstacle density, clearance, target occlusion and speed | Train static point-to-point first; pursuit adds observed target history, moving goals and acceleration limits | Intercept/time-to-contact, collision rate, target-loss duration and replans; distinguish pursuit success from shortest-path success |
| V04 / later | Spacecraft in asteroid fields or station debris: replace scripted obstacle weaving | Ellipsoids, irregular solids, frame structures; aperture/body ratio, speed and turn radius | Velocity-aware state, braking and bounded thrust; curriculum from slow translation to inertial motion; dynamically feasible expert or MPC teacher | Feasible arrival, fuel/control effort, overshoot and near misses; occupancy-only state is insufficient for inertia |
| V05 / after V01 | Doors, moving platforms and destructible obstacles: automate route repair after level changes | V01 worlds plus deterministic obstacle schedules; closure duration, changed-volume fraction, update rate and alternate-route length | Time-indexed occupancy or causal motion observations; waiting action; train on schedules independent of evaluation | Time-to-recover, stale-route collisions, p95 update+replan latency, failure versus proven infeasibility; needs runtime world updates and replayable clocks |
| V06 / after V05 | Multiple flying/swimming NPCs: reduce hand-tuned traffic and bottleneck choreography | Shared portals and intersecting 3D traffic; agent count, opposing-flow fraction and corridor capacity | Joint reservations or local avoidance with neighbor state; freeze priority/fairness rules; single-agent competence first | Throughput, deadlocks, starvation, inter-agent collisions and tail latency; independent shortest paths are not a multi-agent solution |
| V07 / after V01 | Partial-observation exploration: replace scripted search patterns in unknown caves | Identical visible regions with different hidden completions; sensor range, structured missingness and topology | Explicit unknown channel, map memory/belief and frontier baseline; do not provide hidden map to policy; full map only for labels and scoring | Coverage versus travel, collision rate, regret to full-map oracle, calibrated uncertainty; ambiguity should direct information gathering, not fabricated certainty |
| V08 / early offline tool | Navigation QA and change-impact testing: find broken aerial/swimming routes after an edit | Paired original/edited V01/V02 levels; planted blocked portals and valid detours across body sizes | Start with deterministic search, no learning needed; later learn query prioritization from training edits | Defect precision/recall, route coverage, detection time and reproducible traces; timeouts mean unknown, never proof of disconnection |

## Shared Task Contract

Each task manifest must pin source/spec commits, world and generator hashes, split,
seed, voxel-to-world transform, bounds and units, occupancy convention, observation
mask, agent shape, action set, edge costs, timestep, horizon and collision policy.
For dynamic tasks also pin obstacle trajectories, their causal observability,
update timing, agent dynamics and target behavior. Store start/goal, feasibility
status, reference solver and budget, route labels and rejection reasons.

Separate three difficulties: geometry (clearance/topology), route (detour/length),
and control (speed/dynamics/partial observation). Changing all three at once makes
failures uninterpretable. Obstacle density alone is not a difficulty measure.
Do not reject every impossible case: keep a separately labeled infeasible suite
for failure handling. Search timeout is not an infeasibility label.

## Current Implementation Fit

Audited against implementation `155d9e5` on `develop`:
[geometry documentation](https://github.com/amadou-6e/theseo-anysearch/blob/155d9e5/docs/geometries/README.md).
Existing building blocks include STL/box geometry, NPY pools, seeded custom
geometry/scenario providers, finite non-cubic compiled worlds, and bounded A*
task validation. Current descriptors include detour, turns and vertical displacement.
The optional clearance diagnostic uses face-direction queries, not a Euclidean
distance field. Source composition is union-only. None of these establishes
continuous finite-body collision safety, dynamic updates, water/current physics,
or multi-agent reservations.

Prefer the existing pool or compiled-world interfaces for adapters. Do not
convert every occupied voxel into a Python tuple or render mesh simply to import
it. Convert occupancy directly. Coordinates in live Theseo tasks are one-based;
validate the external coordinate convention and record the transform explicitly.

## Training And Evaluation Sequence

### G0: Import And Baseline, No Training

Implement a strict `.3dmap` / `.3dscen` reader and manifest-backed pool/compiler
adapter. Check dimensions, integer bounds, duplicates, matching map names, free
endpoints, NaNs and unexpected format. Test axis ordering with asymmetric fixtures.
Never silently fill cave interiors, wrap negative indices or resize a map.
Preserve source origin when cropping. Seal crop boundaries unless escape is part
of the task, then regenerate queries and references under the new boundaries.

Implement Dijkstra on tiny fixtures and A* on the same validated movement graph.
Check legal diagonal edges and body inflation, then independently replay every
returned path. Supplied benchmark optimum values are usable only after verifying
the benchmark movement rules match; otherwise recompute and label derived tasks.
Review memory requirements before dense allocation: a large benchmark map can
exceed hundreds of millions of cells before channels, labels or search state.
Use small crops first.

### G1: Useful Small Static Flight

Create procedural 33-cubed rooms/portals/shaft and clutter families. Keep the
existing encoder input scale; vary difficulty within it before increasing extent.
Generate training/calibration/test worlds from distinct seeds and reserve a whole
generator variant as OOD. Proposed pilot: 512 training worlds, 128 calibration,
128 test, eight queries each, plus 64 OOD worlds. Freeze counts and splits before
running. Build separate body-radius strata, initially 0, 1 and 2 voxels; radius 0
is a point-agent diagnostic, not the target deployment model.

Compare identical planner/controller paths using (a) raw local occupancy, (b)
spatial features, (c) frozen729 code, (d) shuffled code and (e) no learned guide.
Train a small successor-ranking head from expert suffix costs or imitate legal
expert moves. Keep planner coverage/fallback intact; learned ordering must not
invalidate collision checks or an advertised optimality bound. A learned heuristic
is not admissible merely because it fits reference costs.

Tune head learning rate, width, weight decay and training duration on calibration
worlds only, with equal search budgets per representation. Start with a bounded
12-trial search and three fresh seeds for the selected recipe; freeze an explicit
GPU-hour cap in its issue before execution. This document launches no GPU runs.
Include inference, preprocessing, fallback and data-transfer costs in timing.
Test a raw-input navigation agent trained on the same demonstrations if studying
policy learning, rather than conflating guided-search and policy comparisons.

### G2: One New Mechanism At A Time

Add V02 water-domain restrictions, then V05 one moving blocker, and only then
V06 shared-space traffic or V07 partial observation. Keep static small-world
retention tests. V03/V04 dynamics are separate follow-ups. Do not increase field
of view until the selected small-world application demonstrates utility.

## Evaluation And Decision Rules

These are proposed engineering pilot targets, not literature-established universal
thresholds. Freeze them with budgets before model evaluation; no deployment claim.

| Question | Measurements and proposed decision |
| --- | --- |
| Is the result valid? | Every successful path passes independent swept-body replay; exact agreement with tiny-fixture reference costs; reproducible source/split hashes. Validity failure excludes affected evidence and repairs the harness. |
| Is small static flight usable? | At least 95% success on reference-feasible queries in each frozen body/difficulty stratum; median stretch <=1.10 and p95 <=1.25 on successes, with failures reported separately; zero observed collision on at least 1,000 attempts. Report geometry-cluster confidence intervals; zero observed collisions is not proof of zero risk. |
| Does learning add value? | Against the strongest matched nonlearned/raw baseline, preserve success within a preregistered 2-percentage-point margin and show a positive paired confidence interval for the selected benefit: proposed >=20% median total planning-latency reduction. Include p95 and memory; never claim success from fewer expansions alone. |
| Is it real-time useful? | Publish warm and cold end-to-end p50/p95/p99 latency, updates, concurrency, CPU/GPU allocation and scene load. A provisional 5 ms p95 per-query target requires a named target machine and workload; it is not a universal game frame budget. |
| Does it transfer? | Report per-family/per-radius success, collision, stretch and latency, not just pooled means. OOD failure directs a labeled follow-up and retains the baseline rather than lowering thresholds. |
| What about dynamic scenes? | Report time-indexed collision, recovery latency, arrival, deadlocks and causal sensing. Static A* optimum is not a dynamic-route optimum. |

Cluster resampling uses geometry identity with variants grouped, and multiple
training seeds. Report paired intervals and failure categories. Reference failures
and timeouts stay visible. A visually attractive replay is illustration, not evidence.

## Baseline Ladder And Existing Work

1. Exact grid Dijkstra/A* for correctness; weighted A* for explicit speed-quality
   tradeoffs on the same body/movement rules.
2. An unlearned hierarchical/region planner for large static worlds. Include graph
   construction/update time and resident memory, not just search time.
3. OMPL planning for continuous-body/dynamic feasibility when relevant, using the
   same collision geometry and budgets; its benchmarking facilities support
   reproducible planner comparisons. [OMPL benchmark guide](https://ompl.kavrakilab.org/benchmark.html).
4. Commercial product comparison only when we actually obtain and integrate it:
   Mercuna advertises octree navigation, steering and dynamic avoidance for flying
   and swimming agents. It is a relevant competitor, not a measured baseline in
   our current results. No proprietary binaries/assets downloaded and no speed
   claims against it. [Mercuna](https://mercuna.com/3d-navigation/).

## Asset Library And Provenance

No external assets are acquired by this catalog. Warframe is out of scope and
must not be reacquired ([specs#138](https://github.com/amadou-6e/specs/issues/138)).
Record source, license and hashes for any future asset before use.

| Asset | Role | Access/license and remaining work |
| --- | --- | --- |
| Procedural room/shaft/portal, tube and clutter families | Proposed primary training ground for V01/V02/V03 | Not implemented by this task. Use own seeded generators to control topology. |
| SubT cave/tunnel tiles and worlds | Candidate later geometry source for V02/V07 | Not downloaded. Resolve each model's license and dependencies before acquisition; SDF/world graph needs collision-mesh transforms and voxelization. Its seeded generator exposes cave styles and tile counts. [Official tutorial](https://github.com/osrf/subt/wiki/World-Creation-Tutorial). |

## Execution Packages

| Package | Depends on | Acceptance |
| --- | --- | --- |
| A0 application catalog | None | This document and its review PR |
| A1 importer and coordinate fixtures | A0 | Strict format tests, safe bounded allocation, native occupancy round-trip, matching queries; no training |
| A2 body-safe static baseline | A1 | Tiny-world optimum tests, swept-edge replay, matching reference rules, profiled memory and latency |
| A3 procedural V01 task bank | A2 | Seeded topology/clearance controls, geometry-disjoint splits, manifests and expert paths |
| A4 matched training and small-world assessment | A3 | Frozen search budget/metrics, all controls, fresh-seed evaluation, decision and replays |
| A5 underwater/dynamic follow-ups | A4 | Separate issue and frozen protocol for each new mechanism |

A1 and procedural generator design can proceed independently after A0; A3 label
generation waits for A2. Asset-specific licensing research can run alongside both.
Do not parallelize work that modifies another task's owned importer/contracts.
Create implementation issues before code changes. Perception-specific work uses
the experimental integration line; general geometry infrastructure follows develop
unless its tracking issue establishes the experimental scope. No merges authorized
by this catalog. The immediate next experiment is G1, preceded by A1-A3, not scaling
the encoder or claiming a game-engine integration.
