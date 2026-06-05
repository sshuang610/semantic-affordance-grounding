# Semantic Affordance Grounding — AI Capstone 2026 Homework 5

> **Group 03** &nbsp;·&nbsp; Ontology-based Semantic Grounding of Graspable Objects

A compact, reasoning-driven ontology that lets a robot agent ground perceived
task objects (cups, cutlery, plate, toy blocks, basket) as **typed**,
**role-bearing**, **affordance-carrying** individuals — so an OWL reasoner can
answer: *which objects are graspable, and why?*

---

## 1. Project title and group members

- **Project:** Ontology-based Semantic Grounding for a grasping robot agent
- **Group members:** 徐畹茜 (112550122), 莊蕓安 (112550110), 李尹瑄 (112550032), 黃襄香 (112550123), 曾歆喬 (112550045), 謝欣陵 (112550115)

## 2. Selected task(s)

The baseline object vocabulary for **all three** predefined entry-level tasks is
modeled (required), with **cup stacking** as the primary narrative task:

1. **Cup stacking** — blue cup, pink cup
2. **Cutlery arrangement** — knife, fork, plate
3. **Toy block collection** — toy blocks, basket

## 3. Ontology design (short)

The design separates four semantic layers and never collapses them:

| Layer | Example | Source |
|-------|---------|--------|
| **Object type** | `cap:Cup`, `cap:Knife`, `cap:Basket` | course `cap:` |
| **Task role** | `cap:TargetObject`, `cap:ReferenceObject`, `cap:ContainerTarget`, `cap:CollectableObject` | course `cap:` |
| **Affordance** | `cap:GraspingAffordance`, `cap:SupportAffordance`, `cap:ContainmentAffordance`, `cap:StackabilityAffordance` | course `cap:` |
| **Instance** | `g03:blueCup01`, `g03:knife01`, `g03:basket01` | group `g03:` |
| **Inferred class** | `g03:blueCup01 a cap:GraspableObject` | **reasoner-derived** |

Graspability is **defined**, not listed, by one OWL class axiom:

```
cap:GraspableObject  ≡  cap:PhysicalObject  ⊓  ∃ cap:hasAffordance.cap:GraspingAffordance
```

A reasoner classifies an individual as `cap:GraspableObject` iff it is a physical
object that has at least one grasping affordance. This is why **plate** and
**basket** — which carry support / containment affordances but no grasping
affordance — are correctly **excluded**.

## 4. Modeled objects and their affordances

| Instance | Object type | Task role | Affordance(s) | Inferred graspable? |
|----------|-------------|-----------|---------------|:---:|
| `g03:blueCup01` | `cap:Cup` | TargetObject | Grasping, Stackability | Yes |
| `g03:pinkCup01` | `cap:Cup` | TargetObject | Grasping, Stackability | Yes |
| `g03:knife01` | `cap:Knife` | TargetObject | Grasping | Yes |
| `g03:fork01` | `cap:Fork` | TargetObject | Grasping | Yes |
| `g03:block01` | `cap:ToyBlock` | CollectableObject | Grasping | Yes |
| `g03:block02` | `cap:ToyBlock` | CollectableObject | Grasping | Yes |
| `g03:plate01` | `cap:Plate` | ReferenceObject | Support | No (placement reference) |
| `g03:basket01` | `cap:Basket` | ContainerTarget | Containment | No (container, not grasped) |

## 5. Namespace policy

| Prefix | Namespace | Used for |
|--------|-----------|----------|
| `cap:` | `https://hcis.io/ontology/aicapstone/2026/` | **Shared course vocabulary** (imported, reused as-is). |
| `g03:` | `https://hcis.io/ontology/aicapstone/2026/group03/` | **Group-authored** individuals and affordance instances. |

- The course `cap:` terms are **reused**, never redefined as new group classes.
- All group-specific individuals live under `g03:`.
- The single exception is the **OWL axiom for `cap:GraspableObject`**: we add its
  `owl:equivalentClass` definition. `cap:GraspableObject` is a course-level term,
  so we add only the *axiom* for an existing course term; we do not introduce a
  new class under `cap:`.
- The required OWL/RDFS resources `owl:ObjectProperty`, `owl:DatatypeProperty`,
  and `rdfs:subClassOf` come from the imported `course-affordance.ttl` and are
  reused here via `owl:imports`, rather than re-declared under `g03:`.

## 6. How to run the query

### Files authored by the group vs. imported

- **Authored by Group 03:** [`ontology/group-ontology.ttl`](ontology/group-ontology.ttl),
  all queries, [`src/reason_and_query.py`](src/reason_and_query.py), this README, the report.
- **Imported (provided course resources):**
  [`ontology/imports/course-affordance.ttl`](ontology/imports/course-affordance.ttl)
  and [`ontology/imports/course-alignment.ttl`](ontology/imports/course-alignment.ttl).

### Option A — Protégé + HermiT (primary workflow)

1. Open `ontology/group-ontology.ttl` in **Protégé**. The
   [`ontology/catalog-v001.xml`](ontology/catalog-v001.xml) resolves the
   `owl:imports` to the local `imports/course-affordance.ttl`, so the course
   axioms load even offline.
2. **Reasoner ▸ HermiT ▸ Start reasoner.**
3. Open the **Individuals** tab and confirm that the six objects above show
   `cap:GraspableObject` as an **inferred** type (yellow highlight), while
   `plate01` and `basket01` do not.
4. **File ▸ Export inferred axioms as ontology** → save as
   `ontology/inferred-results.ttl`.
5. **SPARQL Query tab** (or Snap SPARQL): paste
   [`queries/graspable_objects.rq`](queries/graspable_objects.rq) and run it
   *over the inferred model*. Screenshot the result into
   `results/screenshots/`.

### Option B — Python (reproducible verification path)

```bash
pip install rdflib owlrl
python src/reason_and_query.py
```

This loads both ontologies, applies an OWL-RL reasoner, writes
`ontology/inferred-results.ttl`, and writes the query table to
`results/graspable_objects_output.txt`.

## 7. Expected query output

```
object           objectLabel    taskRole
----------------------------------------------------------------
g03:block01      toy_block      cap:CollectableObject
g03:block02      toy_block      cap:CollectableObject
g03:blueCup01    blue_cup       cap:TargetObject
g03:fork01       fork           cap:TargetObject
g03:knife01      knife          cap:TargetObject
g03:pinkCup01    pink_cup       cap:TargetObject
----------------------------------------------------------------
total graspable objects inferred: 6
```

`plate01` and `basket01` are intentionally absent.

## 8. What is inferred, not merely asserted

- We **never** write `g03:blueCup01 a cap:GraspableObject`. No graspability is
  asserted by hand.
- We assert only: each object's **type**, **task role**, and **affordance
  individuals**.
- The reasoner derives `cap:GraspableObject` membership from the
  `owl:equivalentClass` axiom plus the affordance facts. Two complementary
  inference paths reach the same conclusion:
  - **Class-level (DL, HermiT):** every `cap:Cup` is a subclass of
    `cap:PhysicalObject` and carries an existential grasping-affordance
    restriction, so HermiT derives `cap:Cup ⊑ cap:GraspableObject`; every cup
    individual then inherits the inferred type.
  - **Instance-level (OWL-RL):** each graspable instance is explicitly linked to
    a `cap:GraspingAffordance` individual, so the OWL-RL rules
    (`cls-svf1`, `cls-int1`, `cax-eqc`) classify it as `cap:GraspableObject`.

## 9. How `ontology/inferred-results.ttl` was generated

`ontology/inferred-results.ttl` is the **materialized inferred graph**. It is
produced either by **Protégé ▸ File ▸ Export inferred axioms as ontology**
(HermiT) or, reproducibly, by `python src/reason_and_query.py` (owlrl). It
contains the asserted triples plus all derived triples, including the
`a cap:GraspableObject` classifications. It must **not** be edited by hand.

## 10. Links

- Group ontology: [`ontology/group-ontology.ttl`](ontology/group-ontology.ttl)
- Inferred graph: [`ontology/inferred-results.ttl`](ontology/inferred-results.ttl)
- Imported course ontology: [`ontology/imports/course-affordance.ttl`](ontology/imports/course-affordance.ttl)
- Import alignment (SKOS): [`ontology/imports/course-alignment.ttl`](ontology/imports/course-alignment.ttl)
- Main query: [`queries/graspable_objects.rq`](queries/graspable_objects.rq)
- Overview query: [`queries/task_objects.rq`](queries/task_objects.rq)
- Reasoning + query script: [`src/reason_and_query.py`](src/reason_and_query.py)
- Query output: [`results/graspable_objects_output.txt`](results/graspable_objects_output.txt)
- Report: [`report.md`](report.md)
