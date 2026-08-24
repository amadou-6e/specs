# Overview Page — Grid Layout (ASCII)

Columns: 12 equal · Gap: 16px · Margin: 32px each side · Baseline unit: 24px

```
col:  1    2    3    4    5    6    7    8    9   10   11   12
     ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐  ▲
     │ 1  │ 2  │ 3  │ 4  │ 5  │ 6  │ 7  │ 8  │ 9  │ 10 │ 11 │ 12 │  │ 24px  RULER 
     ├────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┤  ▼
     │                                                             │  ▲
     │                         NAV                                 │  │ 48px -- top left should have user icon
     │  BlogHub   Articles  Queue  Platforms  Settings  [+New]     │  ▼
-- visual separator (simply background color)
-- stat bar showing quick info like nr of post this month, connected ai platform
-- visual separator (simply background color)
-- filter bar (filter by blog type and dropdwon for more specific filters)

-- row cards full width
     ├───────────────────────────
     │  platform mono             
     │  Article title italic…     
     │  Category · date · status  
     ├────────────────────────────
     │  platform mono             
     │  Article title italic…     
     │  Category · date · status  
     ├────────────────────────────
     │  platform mono             
     │  Article title italic…     
     │  Category · date · status  
     └───────────────────────────

     ◄── cols 1–6 ──────────────►◄── cols 7–12 ──────────────────►
          article list                     hero
          3 × 72px = 216px               216px = 9×24
```

## Named grid rows

```
[ruler-s]  ──── 24px ────  [ruler-e]
[nav-s]    ──── 48px ────  [nav-e]
[hero-s r1-s] ── 72px ──  [r1-e]
[r2-s]     ──── 72px ────  [r2-e]
[r3-s]     ──── 72px ────  [r3-e hero-e]
```

Hero uses `grid-row: hero-s / hero-e` → spans all 3 article rows = 216px  
Article rows use `grid-row: r1-s / r1-e` etc. → 72px each

## Column split

```
Article body:  grid-column: 1 / 7   (cols 1–6)
Hero:          grid-column: 7 / 13  (cols 7–12)
```
