#!/usr/bin/env python3
"""check_opening_hours.py — the own check of the example specification opening-hours.md.

  no-overlap  within one day, the hours do not overlap, and each one ends after it begins (R4)

Usage:  check_opening_hours.py opening-hours.yml
Exit 0 when clean, 1 with a list of findings otherwise. Validation against the schema (R1, R2) is left to
any JSON Schema validator.
"""
import sys

import yaml


def minutes(t):
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def main():
    data = yaml.safe_load(open(sys.argv[1], encoding="utf-8")) or {}
    days = {**(data.get("weekly") or {}), **(data.get("exceptions") or {})}
    findings = []
    for day, hours in days.items():
        spans = sorted((minutes(a), minutes(b), f"{a}-{b}") for a, b in (h.split("-") for h in hours))
        for start, end, text in spans:
            if end <= start:
                findings.append(f"no-overlap: {day} {text} ends before it begins")
        for (_, end, a), (start, _, b) in zip(spans, spans[1:]):
            if start < end:
                findings.append(f"no-overlap: {day} {a} overlaps {b}")
    for f in findings:
        print(f"fail: {f}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
