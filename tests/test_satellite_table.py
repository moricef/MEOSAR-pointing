#!/usr/bin/env python3
"""Validate the embedded SAR satellite table against the reference CSV."""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "meosar_pointing.py"
REFERENCE = ROOT / "data" / "sar_satellites.csv"


def load_module():
    spec = importlib.util.spec_from_file_location("meosar_pointing", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_reference() -> dict[int, tuple[int, str, str, str]]:
    with REFERENCE.open(newline="", encoding="utf-8") as handle:
        rows = csv.DictReader(handle)
        return {
            int(row["cs_id"]): (
                int(row["norad"]),
                row["constellation"],
                row["label"],
                row["status"],
            )
            for row in rows
        }


def embedded_table(module) -> dict[int, tuple[int, str, str, str]]:
    return {
        sat.cs_id: (sat.norad, sat.constellation, sat.label, sat.status)
        for sat in module.SAR_SATELLITES
    }


def main() -> int:
    module = load_module()
    expected = load_reference()
    actual = embedded_table(module)

    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    mismatches = {
        cs_id: {"expected": expected[cs_id], "actual": actual[cs_id]}
        for cs_id in sorted(set(expected) & set(actual))
        if expected[cs_id] != actual[cs_id]
    }

    if missing or extra or mismatches:
        print(f"missing={missing}")
        print(f"extra={extra}")
        print(f"mismatches={mismatches}")
        return 1

    print(f"SAR satellite table OK: {len(actual)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
