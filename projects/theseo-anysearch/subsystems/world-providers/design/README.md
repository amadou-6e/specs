# World-provider design

## Contained elements

```text
design/
├── 1 README.md
└── 1 python.md
```

Provider orchestration and manifests are Python-owned. Native or third-party tools may
perform conversion, but outputs cross a validated artifact boundary before admission.
