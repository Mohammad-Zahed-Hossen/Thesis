---

## 11. Building a field map

### 11.1 Purpose and size

A field map is **one page** (or two screens) that lets you answer: what do people believe, how do they measure it, what do they disagree about, and where is the frontier? It is a thinking tool, not a bibliography. A 300-entry Zotero library is not a field map; it is a pile. **[L3]**

### 11.2 The ten slots

| Slot | Content | How to fill it fast |
|---|---|---|
| 1. Foundational work | 2–4 papers everyone cites | Follow references from two survey/position papers |
| 2. Recent influential work | 3–6 papers from the last 12–18 months | Sort arXiv by date; check venue accepted lists |
| 3. Competing directions | 2–4 schools of thought | Ask "what do these papers argue against?" |
| 4. Benchmarks | Named evaluation suites | Search `benchmark` + area term; check dataset cards |
| 5. Datasets | Public corpora with provenance | Hugging Face datasets search; dataset cards |
| 6. Common methods | The 3–6 techniques used repeatedly | Method sections of the defining papers |
| 7. Known failure modes | Documented weaknesses of current systems | Limitations sections; error analyses |
| 8. Unresolved questions | Explicitly posed open problems | Limitations + "future work" + position papers |
| 9. Controversies | Where results contradict | Compare papers reporting opposite directions |
| 10. Terminology variants | Different names for the same thing | Track synonyms across communities |

### 11.3 A compact format that works

```text
TERRITORY: <name>

WHAT THE FIELD BELIEVES
  • <claim> — [paper A] — evidence: <one line> — control: yes/no
  • <claim> — [paper B] — evidence: <one line> — control: yes/no

HOW IT MEASURES
  • metric M1 — counts: <what> — weakness: <what it conflates>
  • metric M2 — ...

WHAT IT DISAGREES ABOUT
  • A vs B on <issue> — likely cause of disagreement: <setup difference>

WHAT IT HAS NOT RULED OUT
  • <alternative explanation> — no matched control found on <date of search>

DATA / MODELS / COMPUTE I CAN USE
  • dataset: <name, size, license, inspection status>
  • model: <name, size, VRAM fit>
  • baseline: <what I can reproduce>

MY CANDIDATE QUESTIONS (ranked, with kill reasons)
  1. ...
  2. ...
```

This fits on one screen and is updated in place. **[L3]**

### 11.4 How it evolves

| Stage | Map shape |
|---|---|
| Day 1 | Slots 1, 4, 6 filled crudely; everything else "unknown" |
| Day 3 | Slots 2, 5, 10 filled; slot 8 has candidate questions |
| Day 7 | Slot 3 (competing directions) and slot 7 (failure modes) filled; slot 9 has real disagreements |
| After closest-work search | Slot 8 becomes a ranked list with kill reasons |
| After pilot | Map gains an "evidence from my own data" section |

An empty slot is informative. "I cannot name any controversy in this territory" usually means either the field is stable (good but hard to contribute to) or you have not read enough to see the fault lines. **[L3]**

### 11.5 Building a map in two focused days

**Day 1 (4 hours).**
- Find two recent surveys or position papers; extract slots 1, 3, 6, 8.
- Pull the 6 most-cited recent papers; skim each for slot 7 and their §Limitations.
- Note vocabulary variants as you go (slot 10).

**Day 2 (4 hours).**
- Search benchmarks and datasets; open each dataset card; write one line on provenance and known bias (slots 4, 5).
- Compare two papers that seem to disagree; identify the setup difference (slot 9).
- Write the map in the format above. Mark every uncertain entry with `?`.
- End the day by writing **three candidate questions** and their current kill reasons.

### 11.6 What the map is for

The map is not a deliverable. It is the object you use when deciding:

- Is my question already answered? (§13)
- Which experiment is closest to mine? (§12)
- Do I have the data and compute? (§17)
- Which control would a reviewer demand? (§20)

**Anti-pattern [L2/L3]:** the workspace contains very large audit reports whose size was treated as progress. In practice, the *decisions* they produced were small in number. When the map no longer changes your plan, stop expanding it — that is the signal that exploration has reached diminishing returns.

### 11.7 One more habit: the "frontier date"

Write today's date next to slot 2 and update it whenever you search. If the frontier date is more than a month old, the space may have moved. Before freezing a question, re-run search #10 from §9.1 (recent work) one final time. Half an hour here prevents the worst outcome in §28: writing a full thesis on a question published while you were writing it. **[L3]**
