# MEOSAR Pointing

Lightweight terminal tool for real-time antenna pointing toward MEOSAR
satellites from an amateur radio station.

The main use case is simple: choose a station, list currently visible
MEOSAR satellites, and get azimuth, elevation, range, trend, and remaining
visibility time for manual antenna pointing.

## Install

```bash
python3 -m pip install -r requirements.txt
```

## Quick Start

Pointing table for F4KLO:

```bash
./meosar_pointing.py --qth F4KLO --min-el 10 --pointing
```

Live refresh every 30 seconds:

```bash
./meosar_pointing.py --qth F4KLO --min-el 10 --pointing --watch 30 --clear
```

Track one satellite by Cospas-Sarsat ID:

```bash
./meosar_pointing.py --qth F4KLO --min-el 10 --target 426 --watch 30 --clear
```

Example target output:

```text
MEOSAR TARGET - F4KLO

GSAT0203 - Galileo C/S 426

Azimuth:        60.1 deg
Elevation:      21.2 deg  ↓
Range:         26704 km
Doppler:       -2511 Hz @ 1544.100 MHz
Set:          07:00Z  (38m)
Mask:           10.0 deg
Status:      visible
```

## Stations

Built-in presets:

- `F4KLO`: Radio Club F4KLO, Parc de La Villette, locator `JN18EV64NN`
- `JN02QX`: default test station locator

Any Maidenhead locator can be used:

```bash
./meosar_pointing.py --qth JN18EV64NN --min-el 10 --pointing
```

Latitude/longitude can also be used:

```bash
./meosar_pointing.py --latlon 48.893995 2.387856 --min-el 10 --pointing
```

## Useful Options

- `--pointing`: operator-oriented satellite table.
- `--target ID`: single satellite display by Cospas-Sarsat ID, NORAD ID, or name.
- `--watch SECONDS`: refresh periodically.
- `--clear`: clear the terminal before each refresh.
- `--min-el DEG`: antenna mask / minimum elevation.
- `--doppler-freq-mhz MHz`: receive frequency used for Doppler prediction.
- `--compact`: compact terminal output.
- `--engineering`: show constellation geometry and DOP diagnostics.
- `--json`: machine-readable output.
- `--refresh`: force TLE download.

## 1544 MHz Doppler

The tool predicts the downlink Doppler from the satellite range rate. The
default frequency is `1544.1 MHz`, matching the Galileo SAR downlink commonly
used for F4KLO checks:

```bash
./meosar_pointing.py --qth F4KLO --min-el 10 --target 426 --utc 2026-07-20T06:22:15Z
```

For another receive frequency, for example `1544.5 MHz`:

```bash
./meosar_pointing.py --qth F4KLO --target 426 --doppler-freq-mhz 1544.5
```

The sign convention is receiver-oriented: a positive range rate means the
satellite is moving away, so the received Doppler is negative. This predicts
the satellite-to-station downlink Doppler at the selected receive frequency.
Comparing a measured carrier offset with this prediction leaves the residual
station oscillator error plus any uplink/transponder contribution present in
the received signal.

For example, if a Galileo downlink capture is measured at `-13200 Hz` while the
predicted downlink Doppler is around `-2500 Hz`, the remaining offset is mostly
receiver oscillator error. The beacon-to-satellite uplink Doppler depends on
the beacon location and is not included here.

## Engineering Output

Normal terminal output is focused on antenna pointing and does not show
constellation diagnostics.

For engineering checks:

```bash
./meosar_pointing.py --qth F4KLO --min-el 10 --engineering
```

This adds the geometry summary and DOP values:

```text
Geometry >= 15.0 deg: good  count=13  az_span=284 deg  largest_gap=76 deg  avg_el=38.9 deg
DOP pdop=1.7 hdop=0.9 vdop=1.4 gdop=1.9 tdop=0.9
```

The DOP values are local line-of-sight geometry indicators derived from the
visible MEOSAR satellites. They are useful for engineering comparison between
sky configurations, but they are not operational GNSS receiver PDOP values.

The JSON output always includes the geometry block so that other programs can
consume it:

```bash
./meosar_pointing.py --qth F4KLO --min-el 10 --json
```

## Data Sources

The tool downloads current GNSS TLEs from CelesTrak:

- GPS operational satellites
- Galileo
- GLONASS operational satellites
- BeiDou

It then filters them with an internal list of Cospas-Sarsat MEOSAR-capable
satellites, matched by NORAD catalog number. This list was checked against
`MEOSAR_Satellite_Identification_Parameters_v2026-06-05.xlsx` from the
Cospas-Sarsat MEOSAR satellite identification parameters.

TLE files are cached locally under `~/.cache/meosar-pointing` by default.
If CelesTrak is temporarily unavailable, the tool keeps using the existing
cache when possible.

## Notes

The default display is meant for antenna pointing. Advanced geometry and DOP
information is intentionally hidden unless `--engineering` or `--json` is used.
