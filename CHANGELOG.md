# Changelog

All notable changes to the Surah Gems buying book generator.

## v1.0.0 — 2026-06-22
- Initial release. A5 landscape buying ledger (cover + the system + 50 numbered pages, SG-0001…SG-0500) and a matching supplier receipt pad (R-0001…R-0050).
- Continuous pre-printed serials, shaded value channel, supplier-safe receipt.
- Google Fonts auto-download with offline base-14 fallback.

## v1.1.0 — 2026-06-22
- Added a memo / consignment slip pad (M-0001…M-0050) via `INCLUDE_MEMO_SLIP`:
  declared value, return-by date, and a risk-of-loss line for who carries the
  loss while a stone is in our hands. Output: `SurahGems_MemoSlips_*.pdf`.
- `PURCHASE_MODE` now supports `both`: parcels share a parent serial (SG-0001)
  that splits into children (SG-0001-a, -b, …) in Notion and the media folders
  after sorting. The System page and README document the parcel / Notes guidance.
