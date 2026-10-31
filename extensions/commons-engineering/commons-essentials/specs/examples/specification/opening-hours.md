---
id: opening-hours
title: Opening hours
status: draft
lang: en
touches: [core]
terms: [commons]
schema: opening-hours.schema.json
check: check_opening_hours.py
supersedes: []
---

# Opening hours

*A minimal example of a specification (specification#R13). Any commons that opens its doors can use it.*

## 1 · Goal

A commons states when it is open, so that a person or an agent can decide whether to come now, later or not at all.

## 2 · Boundary

**Belongs here:** the regular weekly hours, and the days that differ from them.

**Does not belong here:** who may enter, bookings, or prices. Where the file lives in the commons is CORE's matter.

## 3 · Terms

No new terms.

## 4 · Requirements

| ID | Level | Requirement | Why | Check |
|---|---|---|---|---|
| R1 | MUST | The opening hours are one file, `opening-hours.yml`, that validates against the schema named in part 5. | One file is found and read the same way by people and agents. | schema |
| R2 | MUST | Each exception names one date and that date's hours, with an empty list meaning closed. | Someone deciding whether to come on a holiday must get that day's answer. | schema |
| R3 | SHOULD | The file is changed before an exception takes effect, not after. | An answer that arrives late changes no decision. | review |
| R4 | MUST | Within one day, the hours do not overlap, and each ends after it begins. | Overlapping hours give two answers to one question. | no-overlap |

## 5 · Structure

The schema is `opening-hours.schema.json`, next to this file.

A day not listed under `weekly` is closed. An exception replaces the weekly hours of its date.

## 6 · Checks

| Check | Tests |
|---|---|
| `schema` | `opening-hours.yml` validates against the schema (R1, R2) |
| `no-overlap` | within one day the hours do not overlap, and each ends after it begins; run by `check_opening_hours.py` (R4) |
| `review` | the human accountable for the opening hours confirms that changes come before they take effect (R3) |

## 7 · Example

The minimal example is also the complete one, since the subject has nothing more:

```yaml
timezone: Europe/Berlin
weekly:
  tue: ["10:00-18:00"]
  sat: ["09:00-13:00"]
exceptions:
  "2026-12-26": []
```

## 8 · Decision log

| Date | Kind | Decision | Word |
|---|---|---|---|
| 2026-10-26 | commissioned | written as the minimal example of the specification rule | commons.o#87 |
