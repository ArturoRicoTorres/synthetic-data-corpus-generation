"""Read-only access to the official BIRD metadata export (data/raw/entities-*.zip).

The zip is extracted once to data/raw/bird_official/ (git-ignored), as src/build_spec_official.py does.
Nothing under data/raw/ is ever modified.
"""
import hashlib
import zipfile
from functools import lru_cache
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
ZIP = Path(sorted(RAW.glob("entities-*.zip"))[-1])
DIR = RAW / "bird_official"


def ensure_extracted():
    if not (DIR / "cube.csv").exists():
        with zipfile.ZipFile(ZIP) as z:
            z.extractall(DIR)


@lru_cache(maxsize=None)
def read(name):
    """One export table as strings, e.g. read("variable")."""
    ensure_extracted()
    return pd.read_csv(DIR / f"{name}.csv", dtype=str, encoding="utf-8-sig", keep_default_na=False)


@lru_cache(maxsize=None)
def indexed(name, key):
    return read(name).drop_duplicates(key).set_index(key)


def zip_sha256():
    return hashlib.sha256(ZIP.read_bytes()).hexdigest()


def algorithm(routine_id):
    text = indexed("routine", "ROUTINE_ID").loc[routine_id, "ALGORITHM"]
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def framework_version(framework_id="FINREP"):
    fv = read("framework_version")
    hit = fv[fv.FRAMEWORK_ID == framework_id]
    return hit.VERSION_ID.iloc[0] if len(hit) else None
