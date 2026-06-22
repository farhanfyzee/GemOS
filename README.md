# Surah Gems — Buying Book

A small, versioned generator that prints a **field buying book** for Surah Gems:
a pre-numbered A5 buying ledger plus a matching supplier-receipt pad, as
print-ready PDFs.

It is a field tool, not a luxury object — navy and black on white, generous
handwriting room, and a single small diamond line-mark on the cover.

> **Surah Gems** is the gem-buying business (rough and cut sapphire and spinel,
> Beruwala, Ceylon). It owns the buying record. **AGTL** (Advanced Gem Testing
> Lab) is a separate lab partner that issues reports and owns those reports.
> The two are kept distinct everywhere — the lab never grades its own stock.

---

## What it produces

`python generate.py` writes these PDFs into `./output/`:

| File | Contents |
| --- | --- |
| `SurahGems_BuyingBook_v{VERSION}_{YYYYMMDD}.pdf` | Cover · The System · every numbered ledger page |
| `SurahGems_Receipts_v{VERSION}_{YYYYMMDD}.pdf` | Every supplier receipt (separate `R-` run) |
| `SurahGems_MemoSlips_v{VERSION}_{YYYYMMDD}.pdf` | Every memo / consignment slip (separate `M-` run) — only when `INCLUDE_MEMO_SLIP = True` |

They are separate print runs by design: the ledger is bound into a book; the
receipts and memo slips are carbon-copy pads.

### Pages

1. **Cover** — wordmark, diamond line-mark, `BUYING LEDGER`, and a
   `Vol. / Year` block. `CONFIDENTIAL — NOT FOR CIRCULATION`.
2. **The System** — a one-page explanation of how the serial, the media
   folders, and the paper/Notion split work (plus parcel and memo guidance
   when those modes are on).
3. **Ledger** (× `LEDGER_PAGES`) — pre-printed serials, an info strip
   (Place / Date / Currency / Page No.), and rows with a shaded **value
   channel** (Asking · My offer · Final buy) bounded by a navy hairline.
4. **Supplier Receipt** (× `RECEIPT_PAGES`) — one per page, minimal: Date,
   Weight, Description, Agreed price, Supplier name, and two signature lines.
   It never shows Asking, My offer, the buying serial, or the buyer's identity.
5. **Memo / consignment slip** (× `MEMO_PAGES`, when `INCLUDE_MEMO_SLIP`) —
   one per page on its own `M-` run: Date, Return-by date, Owner / supplier
   name, Weight, Description, **Declared value**, a **risk-of-loss** line for
   who carries the loss while the stone is in our hands, and two signature
   lines. A memo is *not* a purchase — it never touches the ledger serial.

---

## How to run

```bash
pip install -r requirements.txt      # or: pip install reportlab
python generate.py
```

The PDFs land in `./output/`. Re-running is safe and reproducible — each build
is regenerated from `generate.py` alone, which is why `./output/` and the
downloaded `./fonts/` are git-ignored.

---

## The config block

All variants live at the top of `generate.py` so they can be versioned and
diffed:

```python
SERIAL_PREFIX     = "SG-"      # ledger serial prefix
START_SERIAL      = 1          # first number in the run
ROWS_PER_PAGE     = 10         # rows printed on each ledger page
LEDGER_PAGES      = 50         # → SG-0001 … SG-0500, pre-printed
RECEIPT_PAGES     = 50         # receipt pad length (separate sequence)
RECEIPT_PREFIX    = "R-"       # receipt serial prefix
MEMO_PAGES        = 50         # memo / consignment pad length (separate sequence)
MEMO_PREFIX       = "M-"       # memo serial prefix
CURRENCY_DEFAULT  = "LKR"      # shown in the ledger info strip / memo value
PAGE_SIZE         = "A5"       # A5 | A4 (always landscape)
INCLUDE_MEMO_SLIP = True       # emit the memo / consignment slip pad
PURCHASE_MODE     = "both"     # single | parcel | both
```

`LEDGER_PAGES × ROWS_PER_PAGE` defines the total run length (50 × 10 = 500
serials by default).

---

## The serial system — do not deviate

* **One continuous serial that never resets:** `SG-0001, SG-0002, …`.
* **The date is not in the serial.** It lives only in the Date column and the
  page header. A monthly-reset code would collide across pages — that is why
  the serial must be continuous.
* **Media folder name = serial:** `/Buying/SG-0001/` containing `before/`,
  `after/`, `docs/`.
* The ledger `No.` column is **pre-printed** with the running serial. The
  generator emits a full book of numbered rows so no number can be
  hand-duplicated. **A gap is a void to be accounted for.**
* The receipt pad has its **own** separate `R-` sequence, and the memo pad its
  own `M-` sequence. The three runs never share numbers.

### Parcels (`PURCHASE_MODE = "parcel"` or `"both"`)

A parcel is bought against **one** ledger serial — the **parent** (e.g.
`SG-0001`). After sorting, it splits into **children** — `SG-0001-a`,
`SG-0001-b`, … — recorded in Notion and the media folders, not on a new ledger
row:

```
/Buying/SG-0001/            ← parent (the parcel as bought)
/Buying/SG-0001/SG-0001-a/  ← child after sorting
/Buying/SG-0001/SG-0001-b/
```

The ledger row stays the parent; note the split (and the children) in the
**Notes** column. The children inherit the parent's buy data and gain their own
weight / measurements / report number in Notion. In `single` mode the suffixes
are simply never used.

---

## Font handling

The book uses three Google Fonts:

* **Work Sans** (Regular, Bold) — labels, headers, wordmark
* **Lora** (Regular, Italic) — body prose, footnotes
* **IBM Plex Mono** (Regular) — the folder-tree block

On first run they are downloaded into `./fonts/` and reused thereafter. If a
download fails (e.g. offline), the script falls back to the built-in
Helvetica / Times / Courier families and **never crashes**. Delete `./fonts/`
to force a re-download.

---

## Versioning

* `VERSION` is a constant in `generate.py`.
* The version appears in both output filenames.
* `CHANGELOG.md` gains an entry whenever the version is bumped.
* On the first build the repo is committed and tagged `v{VERSION}` — the
  generator will create the git tag for the current version if it is missing
  (best-effort; it never blocks a build).

Each generation is therefore a tracked release.

---

## Appendix — Notion schema (documented here, not built)

Richer data is entered later in Notion; the paper never duplicates the bench
data. Use **one database, one row per stone**:

| Property | Type | Notes |
| --- | --- | --- |
| Serial | Title | `SG-0001` — matches the paper and the media folder |
| Date | Date | |
| Type | Select / text | sapphire, spinel, … |
| Asking | Number | negotiation trail |
| My offer | Number | negotiation trail |
| Final buy | Number | negotiation trail |
| Supplier | Relation | to a private Suppliers database — code, never name |
| Rough ct | Number | |
| Recut? | Checkbox | |
| Post-recut ct | Number | |
| Measurements | Text | |
| Media | Files / URL | mirrors `/Buying/SG-0001/` |
| AGTL report no. | Text | the lab's number — never assigned by us |
| Status | Select | Bought → Recut → Certified → Delivered |

**Buyer view — important:** do **not** give the buyer database access. Either
export a filtered per-batch PDF (Serial, Type, final weight, measurements,
media, report no.) or use a two-database relation split. Hidden columns in a
Notion view are cosmetic, **not** access control.

---

## Decisions (resolved in v1.1.0)

Both originally-open decisions are now settled and enabled by default:

1. **`INCLUDE_MEMO_SLIP = True`** — yes, we take stones on memo / consignment,
   so the generator emits a memo-slip pad (`M-` run) with declared value,
   return-by date, and a risk-of-loss line for who carries the loss while a
   stone is in our hands. Set it back to `False` to skip that pad.
2. **`PURCHASE_MODE = "both"`** — we buy single stones *and* parcels. A parcel
   serial is a parent (`SG-0001`) that splits into children (`SG-0001-a`,
   `-b`, …) after sorting; see [Parcels](#parcels-purchase_mode--parcel-or-both).
   Use `"single"` or `"parcel"` to narrow the guidance.
