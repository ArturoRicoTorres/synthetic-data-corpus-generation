"""Rule 6: artifacts the classifier will see carry no part of the answer key."""
import re

import pytest

from conftest import ROOT, SQL_DIR

CORPUS = sorted(SQL_DIR.glob("*.sql")) + [ROOT / "sql" / "corrections.yaml"]


def forbidden_patterns(spec):
    pats = [r"\bT\d{2}\b", r"gap_fill", r"business_group", r"taxonomy"]
    for label in spec["taxonomy_draft"]:
        words = label.lower().split("_")
        pats.append(r"\b" + r"[\s_]+".join(map(re.escape, words)) + r"\b")
    return [re.compile(p, re.IGNORECASE) for p in pats]


@pytest.mark.parametrize("path", CORPUS, ids=[p.name for p in CORPUS])
def test_no_answer_key_terms(spec, path):
    text = path.read_text(encoding="utf-8")
    hits = [(p.pattern, m.group(0)) for p in forbidden_patterns(spec) for m in p.finditer(text)]
    assert not hits, f"{path.name}: {hits}"


def test_lineage_map_is_not_in_the_corpus():
    assert (ROOT / "sql" / "lineage_map.yaml") not in CORPUS
