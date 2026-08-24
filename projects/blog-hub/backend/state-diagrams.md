# State Diagrams

Entity lifecycle state machines for the BlogHub backend, derived from actual screen
behaviour (editor v2, create-article v1, overview v4).

---

## Article

![diagram-1](assets/state-diagrams/diagram-1.png)

---

## Destination (per-article, per-platform)

Each article has one `PlatformSummary` per enabled platform.

![diagram-2](assets/state-diagrams/diagram-2.png)

---

## Gate (inspection result per article)

![diagram-3](assets/state-diagrams/diagram-3.png)

---

## Comment

![diagram-4](assets/state-diagrams/diagram-4.png)

---

## Patch

![diagram-5](assets/state-diagrams/diagram-5.png)

---

## Job

![diagram-6](assets/state-diagrams/diagram-6.png)

---

## Connection

![diagram-7](assets/state-diagrams/diagram-7.png)
-> fail : POST /api/articles/{id}/inspect → word count < 500

  pass --> pending : article body changed (autosave)
  warn --> pending : article body changed (autosave)
  fail --> pending : article body changed (autosave)
```

---

## Comment

![diagram-4](assets/state-diagrams/diagram-4.png)

---

## Patch

![diagram-5](assets/state-diagrams/diagram-5.png)

---

## Job

![diagram-6](assets/state-diagrams/diagram-6.png)

---

## Connection

![diagram-7](assets/state-diagrams/diagram-7.png)
