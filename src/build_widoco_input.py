#!/usr/bin/env python3
"""
build_widoco_input.py
=====================
Produce a single, self-contained ontology file for Widoco documentation.

`group-ontology.ttl` uses owl:imports to pull in the course vocabulary, but
the import IRI (https://hcis.io/ontology/aicapstone/2026) is not resolvable
online, so Widoco cannot fetch it. This script merges the imported course
ontology and the group ontology into one graph, drops the owl:imports triple,
and removes the *course* ontology header so the merged file is documented as
the single Group 03 ontology with all course terms inlined.

Output: build/group-ontology-merged.ttl  (used only as Widoco input;
the submitted group-ontology.ttl is unchanged).

Usage:
    pip install rdflib
    python src/build_widoco_input.py
"""
from pathlib import Path
from rdflib import Graph, URIRef
from rdflib.namespace import OWL

REPO = Path(__file__).resolve().parent.parent
COURSE_FILE = REPO / "ontology" / "imports" / "course-affordance.ttl"
GROUP_FILE = REPO / "ontology" / "group-ontology.ttl"
OUT = REPO / "build" / "group-ontology-merged.ttl"

COURSE_ONT = URIRef("https://hcis.io/ontology/aicapstone/2026")
GROUP_ONT = URIRef("https://hcis.io/ontology/aicapstone/2026/group03")


def main() -> None:
    g = Graph()
    g.parse(COURSE_FILE, format="turtle")
    g.parse(GROUP_FILE, format="turtle")

    # The course vocabulary is now inlined, so drop the import...
    g.remove((GROUP_ONT, OWL.imports, None))
    # ...and remove the course ontology's own header so there is exactly one
    # owl:Ontology (the group's) for Widoco to document.
    for p, o in list(g.predicate_objects(COURSE_ONT)):
        g.remove((COURSE_ONT, p, o))

    OUT.parent.mkdir(exist_ok=True)
    g.serialize(destination=str(OUT), format="turtle")
    print(f"merged -> {OUT.relative_to(REPO)} | triples: {len(g)}")


if __name__ == "__main__":
    main()
