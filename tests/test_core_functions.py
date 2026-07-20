#!/usr/bin/env python3
"""Smoke tests for core MEOSAR pointing helper functions."""

from __future__ import annotations

import datetime as dt
import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "meosar_pointing.py"


class FakeDistance:
    def __init__(self, km: float):
        self.km = km


class FakeAngle:
    degrees = 0.0


class FakeTopocentric:
    def __init__(self, km: float):
        self._km = km

    def altaz(self):
        return FakeAngle(), FakeAngle(), FakeDistance(self._km)


class FakeDifference:
    def at(self, time):
        return FakeTopocentric(20_000.0 + time.offset_seconds * 0.5)


class FakeSatellite:
    def __sub__(self, observer):
        return FakeDifference()


class FakeTimescale:
    def __init__(self, center: dt.datetime):
        self.center = center

    def from_datetime(self, value: dt.datetime):
        class FakeTime:
            pass

        fake = FakeTime()
        fake.offset_seconds = (value - self.center).total_seconds()
        return fake


def load_module():
    spec = importlib.util.spec_from_file_location("meosar_pointing", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def approx(value: float, expected: float, tolerance: float) -> None:
    assert abs(value - expected) <= tolerance, (value, expected, tolerance)


def test_maidenhead(module) -> None:
    lat, lon = module.maidenhead_to_latlon("JN18EV64NN")
    approx(lat, 48.8940104167, 1e-9)
    approx(lon, 2.3880208333, 1e-9)


def test_target_and_constellation_filters(module) -> None:
    galileo_426 = next(sat for sat in module.SAR_SATELLITES if sat.cs_id == 426)
    assert module.target_matches(galileo_426, "426")
    assert module.target_matches(galileo_426, "40544")
    assert module.target_matches(galileo_426, "GSAT0203")
    assert not module.target_matches(galileo_426, "502")

    bds = module.selected_sar_satellites("bds")
    assert {sat.cs_id for sat in bds} == {631, 632, 633, 638, 639, 640}


def test_format_duration(module) -> None:
    assert module.format_duration(None) == "--"
    assert module.format_duration(30) == "<1m"
    assert module.format_duration(90) == "2m"
    assert module.format_duration(3 * 3600 + 2 * 60) == "3h02"


def test_doppler_sign_and_scale(module) -> None:
    center = dt.datetime(2026, 7, 20, 6, 22, 15, tzinfo=dt.timezone.utc)
    range_rate, doppler = module.doppler_at(
        FakeSatellite(),
        observer=object(),
        ts=FakeTimescale(center),
        start=center,
        frequency_mhz=1544.1,
    )
    approx(range_rate, 500.0, 1e-9)
    approx(doppler, -2575.28, 0.01)


def main() -> int:
    module = load_module()
    tests = [
        test_maidenhead,
        test_target_and_constellation_filters,
        test_format_duration,
        test_doppler_sign_and_scale,
    ]
    for test in tests:
        test(module)
    print(f"Core helper tests OK: {len(tests)} tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
