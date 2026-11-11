"""Rule 6 / decision D6: nothing of the answer key reaches the corpus the classifier sees."""
import re

import pytest
import yaml

from conftest import ROOT

CORPUS_FILES = sorted(p for p in (ROOT / "corpus").rglob("*") if p.is_file())
TEXT_DIR = ROOT / "src" / "corpus_text"


def labels(spec):
    return [k.lower().split("_") for k in spec["taxonomy_draft"]]


def forbidden(spec):
    pats = [r"\bT\d{2}\b", r"gap_fill", r"business_group", r"taxonomy", r"\bOI-\d{2}\b", r"answer_key",
            r"lineage_map", r"corrections\.yaml"]
    flags = []
    for words in labels(spec):
        if len(words) > 1:          # multi-word labels: blocked as a phrase, any case
            flags.append((r"\b" + r"[\s_-]+".join(map(re.escape, words)) + r"\b", re.I))
        else:                        # single-word labels: blocked only in label form (D6)
            w = re.escape(words[0])
            flags.append((rf"\b{w.upper()}\b", 0))
            flags.append((rf"^#+\s*{w}\s*$", re.I | re.M))
            flags.append((rf'"\s*{w}\s*"', re.I))
    return [re.compile(p) for p in pats] + [re.compile(p, f) for p, f in flags]


@pytest.mark.parametrize("path", CORPUS_FILES, ids=[p.relative_to(ROOT).as_posix() for p in CORPUS_FILES])
def test_no_answer_key_terms(spec, path):
    text = path.read_text(encoding="utf-8")
    hits = [(p.pattern, m.group(0)) for p in forbidden(spec) for m in p.finditer(text)]
    assert not hits, hits[:5]


def test_no_taxonomy_definitions_or_node_names(spec):
    norm = lambda s: re.sub(r"\s+", " ", s).strip().lower()  # noqa: E731
    phrases = [norm(d) for d in spec["taxonomy_draft"].values()] + [norm(t["name"]) for t in spec["transformations"]]
    for path in CORPUS_FILES:
        text = norm(path.read_text(encoding="utf-8"))
        assert not [p for p in phrases if p in text], path.name


def strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from strings(v)


def test_hand_written_prose_avoids_label_words(spec):
    """Prose written for the corpus avoids even the single label words (D6)."""
    words = [w[0] for w in labels(spec) if len(w) == 1]
    for f in TEXT_DIR.glob("*.yaml"):
        if f.name == "legal_extracts.yaml":      # configuration only; quoted text comes from the legal source
            continue
        for s in strings(yaml.safe_load(f.read_text(encoding="utf-8"))):
            hits = [w for w in words if re.search(rf"\b{w}", s, re.I)]
            assert not hits, f"{f.name}: {hits} in {s[:80]!r}"


def test_answer_key_is_outside_the_corpus():
    assert not (ROOT / "corpus" / "answer_key").exists()
    assert (ROOT / "answer_key" / "sql_object_map.yaml").exists()
