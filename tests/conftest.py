import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import generate_synthetic  # noqa: E402

SPEC_PATH = ROOT / "specs" / "npl_ratio_lineage_spec_v0.2.yaml"
SQL_DIR = ROOT / "sql" / "reference"


@pytest.fixture(scope="session")
def spec():
    return yaml.safe_load(open(SPEC_PATH, encoding="utf-8"))


@pytest.fixture(scope="session")
def synthetic(tmp_path_factory):
    """Factory: synthetic data directory for a seed, generated once per test session."""
    cache = {}

    def make(seed=42):
        if seed not in cache:
            cache[seed] = generate_synthetic.generate(tmp_path_factory.mktemp(f"seed{seed}"), seed=seed)
        return cache[seed]

    return make
