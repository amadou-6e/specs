# Perception encoder state and review

Snapshot: 2026-09-08. Review repairs: specs#25 and theseo-anysearch#350.
Governing predecessor spec: `d9b260a5c677277d47776c7677fe07c2a7ff4f34`.
Reviewed implementation: `a2e9f5a87066ed663f7ea76f318d09b9177d115b`.
This snapshot is a review artifact, not an experiment result or a new run.

```mermaid
flowchart TD
    V1["v1 P1 executed<br/>Original verdict superseded"]
    V21["v2r1 P0C completed<br/>Reachability gap 0.0662 below 0.10"]
    STOP["v2r1 terminal<br/>P0D blocked; replacement P1 not started"]
    SPEC["v2r2 methodology merged<br/>Exploratory infrastructure retained"]
    FIX["Review repairs #350 and specs#25<br/>Proposed: code, evidence checks, audit rules"]
    NOW["#340 pending<br/>Implement and freeze audit contract"]
    R0{"R0: sufficient evidence<br/>of usable topology signal?"}
    CAL["P0C calibration<br/>Sampler, controls, structural probes, primary metric"]
    FREEZE["Freeze comparative contract<br/>Require valid topology component"]
    SENS{"P0D sensitivity passes?"}
    P1["P1-P2: training approach"]
    P4["P3-P4: architecture comparison"]
    LATER["P5-P8: context, interactions,<br/>confirmation, scaling smoke"]
    END["Stop; record reason<br/>No topology: no_topology_identifiable<br/>Other gate failure: blocked"]
    LOCAL["#341 separately proposable<br/>Only after no_topology_identifiable"]
    V1 --> V21 --> STOP
    STOP -. successor .-> SPEC --> FIX --> NOW --> R0
    R0 -- feasible --> CAL --> FREEZE --> SENS
    R0 -- defer --> END
    CAL -- invalid topology --> END
    SENS -- fail --> END
    SENS -- pass --> P1 --> P4 --> LATER
    END -. separate program .-> LOCAL
    style STOP fill:#fde2e2,stroke:#b42318
    style END fill:#fde2e2,stroke:#b42318
    style FIX fill:#fff3cd,stroke:#997300
    style NOW fill:#fff3cd,stroke:#997300
    style SPEC fill:#dcfce7,stroke:#15803d
```

## Evidence and implications

| v2r1 component | Floor | Reference | Calibration outcome |
| --- | ---: | ---: | --- |
| Occupied IoU | 0.5974 | 0.9551 | Passed |
| Boundary F1 | 0.5913 | 0.9864 | Passed |
| Clearance NMAE (lower is better) | 0.2231 | 0.0913 | Passed |
| Reachability AUPRC | 0.9309 | 0.9971 | Failed 0.10 headroom |
| Geodesic NMAE | - | - | Deferred |

The reachability floor was coordinates-only. The result does not establish
linear decodability of connectivity from raw occupancy. The archived report is
`experiments/perception_encoder/results/v2r1_p0c/p0c-report.json` in the reviewed
implementation commit; payload hash:
`2564db175a1880cf81da40bd5a32e472f9b3db81bce111283fe48c74d409697b`.

## Repair inventory

1. Correct the coordinates-only diagnosis and require a sampling-shortcut audit.
2. Count unknown cells on a deterministic shortest path. The old union-of-paths
   implementation reports seven on a 3x3 open grid where every shortest path
   crosses exactly three unknown interior cells. Historical screen values stay
   non-evidential and must not be reused for v2r2 strata or thresholds.
3. Explicitly supersede the old absolute false-open and aggregate-score vetoes
   for v2r2; retain state, mask, collapse, and resource checks.
4. Require resolved numeric audit parameters, uncertainty handling, and a fixed
   primary-metric selection rule before R0. Use log base 2 for log-loss headroom.
5. Exclude entire geometry groups, including counterfactual siblings, from
   reference fitting. Keep oracle-completed inputs out of the gating reference.
6. Recompute report payload hashes before accepting prerequisite evidence.

The v2r2 topology helper is present, but its audit and comparative contract
integration is #340 work. A helper alone does not enforce the experiment boundary.
The future audit's numeric choices require review before data are opened; this
repair does not claim R0 has run or that topology is identifiable.
