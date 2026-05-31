#!/usr/bin/env python3
"""
reason_and_query.py
===================
Reproducible reasoning + query pipeline for Homework 5.

What it does:
  1. Loads the imported course ontology (cap:) and the group ontology (grp:).
  2. Materializes inferred triples with an OWL-RL reasoner (the `owlrl`
     library), which applies the OWL 2 RL rules cls-svf1, cls-int1, and
     cax-eqc that classify individuals under cap:GraspableObject from the
     owl:equivalentClass / owl:intersectionOf / owl:someValuesFrom axiom.
  3. Exports the inferred graph to ontology/inferred-results.ttl.
  4. Runs queries/graspable_objects.rq over the inferred graph and writes
     the table to results/graspable_objects_output.txt.

This is the Python verification / reproducibility path. The PRIMARY
submission story uses Protege + HermiT (an OWL 2 DL reasoner) for
screenshots and inferred-axiom export; this script independently confirms
that the same individuals are classified as cap:GraspableObject.

Usage:
    pip install rdflib owlrl
    python src/reason_and_query.py
"""
from pathlib import Path
import rdflib
from rdflib import Graph
import owlrl

# Resolve paths relative to the repository root (parent of this src/ dir),
# so the script works no matter what the current working directory is.
REPO = Path(__file__).resolve().parent.parent
COURSE = REPO / "ontology" / "imports" / "course-affordance.ttl"
GROUP = REPO / "ontology" / "group-ontology.ttl"
INFERRED = REPO / "ontology" / "inferred-results.ttl"
QUERY = REPO / "queries" / "graspable_objects.rq"
OUT = REPO / "results" / "graspable_objects_output.txt"

CAP = "https://hcis.io/ontology/aicapstone/2026/"


def short(term) -> str:
    """Abbreviate full IRIs with their namespace prefix for readable output."""
    s = str(term)
    if s.startswith(CAP + "group"):
        # grp namespace: .../groupXX/blueCup01 -> grp:blueCup01
        return "g03:" + s.rsplit("/", 1)[-1]
    if s.startswith(CAP):
        return "cap:" + s[len(CAP):]
    return s


def main() -> None:
    g = Graph()
    print(f"[load] {COURSE.name}")
    g.parse(COURSE, format="turtle")
    print(f"[load] {GROUP.name}")
    g.parse(GROUP, format="turtle")
    asserted = len(g)
    print(f"[load] asserted triples: {asserted}")

    print("[reason] applying OWL-RL closure ...")
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
    print(f"[reason] total triples after inference: {len(g)} (+{len(g) - asserted})")

    g.serialize(destination=str(INFERRED), format="turtle")
    print(f"[write] inferred graph -> {INFERRED.relative_to(REPO)}")

    query_text = QUERY.read_text(encoding="utf-8")
    results = list(g.query(query_text))

    # Build a readable, reproducible text table.
    lines = []
    lines.append("Inferred graspable objects (query: queries/graspable_objects.rq)")
    lines.append("Reasoner: owlrl OWL-RL closure over course + group ontology")
    lines.append("=" * 64)
    header = f"{'object':<16} {'objectLabel':<14} {'taskRole':<22}"
    lines.append(header)
    lines.append("-" * 64)
    for row in results:
        obj = short(row.obj)
        label = str(row.label) if row.label else ""
        role = short(row.role) if row.role else ""
        lines.append(f"{obj:<16} {label:<14} {role:<22}")
    lines.append("-" * 64)
    lines.append(f"total graspable objects inferred: {len(results)}")

    table = "\n".join(lines)
    print("\n" + table)
    OUT.write_text(table + "\n", encoding="utf-8")
    print(f"\n[write] query output -> {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
