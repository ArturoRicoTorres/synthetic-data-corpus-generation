"""The SQL result equals the independent pandas/Python result, cell by cell."""
from decimal import Decimal

import pytest

import reference_calc
import run_reference_sql

SEEDS = [42, 7]


def as_decimal(x):
    return None if x is None else Decimal(str(x))


@pytest.fixture(scope="module")
def results(synthetic):
    """SQL and independent results per seed, computed once (the view chain is re-expanded on every query)."""
    cache = {}

    def get(seed):
        if seed not in cache:
            data = synthetic(seed)
            cache[seed] = run_reference_sql.run(data), reference_calc.run(data)
        return cache[seed]

    return get


@pytest.mark.parametrize("seed", SEEDS)
def test_sql_equals_independent_calculation(results, seed):
    sql, py = results(seed)
    assert sql.keys() == py.keys()
    for ctx in sql:
        assert as_decimal(sql[ctx]["C0010"]) == py[ctx]["C0010"], ctx
        assert as_decimal(sql[ctx]["C0060"]) == py[ctx]["C0060"], ctx
        a, b = as_decimal(sql[ctx]["NPL_RATIO"]), py[ctx]["NPL_RATIO"]
        assert (a is None and b is None) or abs(a - b) <= Decimal("1e-12"), ctx


@pytest.mark.parametrize("seed", SEEDS)
def test_results_are_not_trivial(results, seed):
    sql, _ = results(seed)
    for ctx in ("IFRS", "NGAAP"):
        assert sql[ctx]["C0010"] > 0 and 0 < sql[ctx]["C0060"] < sql[ctx]["C0010"]
    assert sql["SCHEME4"] == {"C0010": None, "C0060": None, "NPL_RATIO": None}
