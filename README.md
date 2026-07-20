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
- `--compact`: compact terminal output.
- `--json`: machine-readable output.
- `--refresh`: force TLE download.

## Data Sources

The tool downloads current GNSS TLEs from CelesTrak:

- GPS operational satellites
- Galileo
- GLONASS operational satellites

It then filters them with an internal list of Cospas-Sarsat MEOSAR-capable
satellites, matched by NORAD catalog number.

TLE files are cached locally under `~/.cache/meosar-pointing` by default.
If CelesTrak is temporarily unavailable, the tool keeps using the existing
cache when possible.

## Notes

The default display is meant for antenna pointing. Advanced geometry and DOP
information is available in the detailed and JSON output, but it is not needed
for normal manual pointing.
