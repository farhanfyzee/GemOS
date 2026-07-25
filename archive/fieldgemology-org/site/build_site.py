#!/usr/bin/env python3
"""
Build the interactive study site for the fieldgemology.org archive.

Reads every *.md file under ../ (archive/fieldgemology-org/**), dedupes the
site-wide chrome (nav/disclaimer header + sidebar footer that repeats on
almost every 2005-2016-era page) into a shared block table, rewrites
internal links into in-app navigation, and embeds everything (gzip-
compressed) plus three self-hosted fonts into a single self-contained
index.html next to this script.

Run: python3 build_site.py   (needs: pip install beautifulsoup4 html2text markdown)
"""
import base64
import gzip
import html
import json
import os
import re
import glob
import urllib.request
from urllib.parse import urlparse, urljoin, unquote

from bs4 import BeautifulSoup
import html2text
import markdown as mdlib

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE = os.path.dirname(SITE_DIR)          # archive/fieldgemology-org/
FONTS_DIR = os.path.join(SITE_DIR, "fonts")  # git-ignored local cache

# --------------------------------------------------------------------------- #
# Fonts — same resilient download-with-fallback pattern as ../../generate.py
# --------------------------------------------------------------------------- #
_R = "https://raw.githubusercontent.com"
FONT_SPECS = {
    "Lora-Regular": f"{_R}/cyrealtype/Lora-Cyrillic/master/fonts/ttf/Lora-Regular.ttf",
    "Lora-Bold": f"{_R}/cyrealtype/Lora-Cyrillic/master/fonts/ttf/Lora-Bold.ttf",
    "WorkSans-Regular": f"{_R}/weiweihuanghuang/Work-Sans/master/fonts/ttf/WorkSans-Regular.ttf",
    "WorkSans-SemiBold": f"{_R}/weiweihuanghuang/Work-Sans/master/fonts/ttf/WorkSans-SemiBold.ttf",
    "IBMPlexMono-Regular": f"{_R}/google/fonts/main/ofl/ibmplexmono/IBMPlexMono-Regular.ttf",
}

def fetch_fonts():
    os.makedirs(FONTS_DIR, exist_ok=True)
    b64 = {}
    for key, url in FONT_SPECS.items():
        dest = os.path.join(FONTS_DIR, key + ".ttf")
        if not os.path.exists(dest):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=25) as resp:
                    data = resp.read()
                with open(dest, "wb") as fh:
                    fh.write(data)
            except Exception as exc:
                print(f"  font download failed for {key}: {exc} (page will fall back to system fonts)")
                b64[key] = ""
                continue
        b64[key] = base64.b64encode(open(dest, "rb").read()).decode("ascii")
    return b64

# --------------------------------------------------------------------------- #
# Front matter
# --------------------------------------------------------------------------- #
FRONT_RE = re.compile(r"^---\n(.*?)\n---\n\n?", re.S)

def parse_front(txt):
    m = FRONT_RE.match(txt)
    if not m:
        return {}, txt
    meta = {}
    for line in m.group(1).split("\n"):
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        if v.startswith('"') and v.endswith('"'):
            v = v[1:-1]
        meta[k.strip()] = v
    return meta, txt[m.end():]

# --------------------------------------------------------------------------- #
# Titles
# --------------------------------------------------------------------------- #
GENERIC_TITLE_RE = re.compile(r"where passion for gemology", re.I)

MANUAL_TITLES = {
    "01-original-site-2005-2009/biography-vincent-pardieu": "About the Author: Vincent Pardieu",
    "01-original-site-2005-2009/expeditions/tajikistan-ruby-2011": "Tajikistan: Ruby (2011 update)",
}

def slug_to_title(pid):
    base = pid.rsplit("/", 1)[-1]
    words = re.split(r"[-_]+", base)
    small = {"and", "or", "the", "of", "to", "a", "an", "in"}
    out = []
    for i, w in enumerate(words):
        if not w:
            continue
        out.append(w.lower() if (w.lower() in small and i != 0) else (w[:1].upper() + w[1:]))
    return " ".join(out)

def resolve_title(pid, meta_title, inv, category):
    if pid in MANUAL_TITLES:
        return MANUAL_TITLES[pid]
    is_generic = (not meta_title) or GENERIC_TITLE_RE.search(meta_title)
    if category == "blog-post":
        key = inv.get("title", "")
        if key:
            return slug_to_title(re.sub(r"[^a-zA-Z0-9]+", "-", key))
    if category == "wp-core":
        return f"Site placeholder — “Coming back soon” ({slug_to_title(pid)})"
    if category == "homepage":
        return "fieldgemology.org — homepage"
    return slug_to_title(pid) if is_generic else meta_title

# --------------------------------------------------------------------------- #
# Link / image resolution
# --------------------------------------------------------------------------- #
def norm_path(url):
    try:
        p = urlparse(url)
    except Exception:
        return None
    path = unquote(p.path).lower()
    if path.endswith("/") and len(path) > 1:
        path = path[:-1]
    key = path
    if p.query:
        m = re.search(r"key=([^&]+)", p.query, re.I)
        key += "?key=" + unquote(m.group(1)).lower() if m else "?" + p.query.lower()
    return key

ALIASES = {
    "/blog_display.php?key=congress": "02-blog-2009-2016/posts/congress",
    "/blog_display.php?key=khao ploy waen": "02-blog-2009-2016/posts/khao-ploy-waen",
    "/blog_display.php?key=sapphire": "02-blog-2009-2016/posts/sapphire",
}

LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(((?:\\.|[^)])+?)(?:\s+\"[^\"]*\")?\)")
AUTOLINK_RE = re.compile(r"<(https?://[^>\s]+)>")

def unescape_url(u):
    """html2text backslash-escapes literal parens inside a URL so they
    don't get mistaken for the closing ')' of the markdown link — undo
    that once the URL has been captured out."""
    return u.replace("\\(", "(").replace("\\)", ")")
STRAY_PIPE_RE = re.compile(r"^[\s|]+$")

def strip_stray_pipes(text):
    """html2text leaves lone-pipe artifacts from the site's nested-table
    layout (empty cells, or a table row split from its header by the block
    splitter). None of these carry information, so drop them."""
    lines = [ln for ln in text.split("\n") if not STRAY_PIPE_RE.match(ln)]
    text = "\n".join(lines)
    text = re.sub(r"^(\s*)\|\s*\|\s*", r"\1", text)
    text = re.sub(r"^(#{1,6}\s*)\|\s*", r"\1", text)
    text = re.sub(r"^\s*\|\s+(?=\S)", "", text)
    return text

# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #
def build():
    inventory = json.load(open(f"{ARCHIVE}/inventory.json"))
    inv_by_relpath = {e["relpath"]: e for e in inventory}

    files = sorted(f for f in glob.glob(f"{ARCHIVE}/**/*.md", recursive=True) if not f.endswith("/README.md"))

    pages = {}
    for f in files:
        rel = os.path.relpath(f, ARCHIVE)
        pid = rel[:-3]
        meta, body = parse_front(open(f, encoding="utf-8").read())
        inv = inv_by_relpath.get(rel, {})
        category = inv.get("category", "")
        pages[pid] = dict(
            relpath=rel,
            title=resolve_title(pid, meta.get("title", ""), inv, category),
            source_url=meta.get("source_url", ""),
            capture_date=meta.get("capture_date", ""),
            wayback_snapshot=meta.get("wayback_snapshot", ""),
            site_era=meta.get("site_era", ""),
            category=category,
            body=body,
        )
    print("pages parsed:", len(pages))

    path_to_id = {}
    for pid, pg in pages.items():
        k = norm_path(pg["source_url"])
        if k and k not in path_to_id:
            path_to_id[k] = pid
    for k, v in ALIASES.items():
        path_to_id.setdefault(k, v)

    # The live fieldgemology.org domain is dead / squatted by an unrelated
    # party today (see README "Death and domain drift"), so a link to any
    # fieldgemology.org page we did NOT individually archive must never
    # point at the live domain — it has to resolve to an actual Wayback
    # Machine capture instead. Build that lookup from the full, unfiltered
    # CDX index (cdx_full_index.json) captured during the original archive
    # pass, so no extra network calls are needed at build time.
    cdx_rows = json.load(open(f"{ARCHIVE}/cdx_full_index.json"))
    cdx_by_path = {}
    for ts, orig, status, mime in cdx_rows[1:]:
        if status != "200":
            continue
        k = norm_path(orig)
        if not k:
            continue
        cdx_by_path.setdefault(k, []).append((ts, orig))
    for k in cdx_by_path:
        cdx_by_path[k].sort()

    def closest_wayback_url(target_url, near_ts):
        k = norm_path(target_url)
        candidates = cdx_by_path.get(k)
        if not candidates:
            # never captured under this exact path/query — hand off to
            # Wayback's own "nearest capture" redirect rather than a dead
            # direct link.
            year = (near_ts or "2015")[:4]
            return f"https://web.archive.org/web/{year}/{target_url}"
        near = near_ts or "20150101"
        ts, orig = min(candidates, key=lambda c: abs(int(c[0][:8]) - int(near[:8])))
        return f"https://web.archive.org/web/{ts}/{orig}"

    def resolve_link(href, base_url, capture_ts=None, own_pid=None):
        href = href.strip()
        if not href:
            return None
        if href.startswith("#"):
            # A same-page anchor in the original (e.g. a table-of-contents
            # jump to "#introduction"). We don't carry per-heading anchor
            # ids into the reader, so the only safe resolution is "this
            # page" — never let it fall through to urljoin, which would
            # silently reconstruct a full link to the live (squatted)
            # fieldgemology.org domain.
            return ("internal", own_pid) if own_pid else None
        try:
            absu = urljoin(base_url, href)
        except Exception:
            return None
        k = norm_path(absu)
        if k in path_to_id:
            return ("internal", path_to_id[k])
        if "fieldgemology" in urlparse(absu).netloc.lower():
            return ("wayback", closest_wayback_url(absu, capture_ts))
        return None

    def resolve_href_out(href, base_url, capture_ts=None, own_pid=None):
        """Absolute, always-usable href for a link: in-app route for pages we
        archived, an actual Wayback Machine snapshot for other
        fieldgemology.org URLs (never the live domain — it's squatted by an
        unrelated party today), or the original target resolved to an
        absolute URL otherwise. Never returns a bare relative path — those
        go nowhere from inside this single page."""
        res = resolve_link(href, base_url, capture_ts, own_pid)
        if res is None:
            if href.startswith("#"):
                return "#/about"  # no page context to anchor to; don't leak a live URL
            # resolve_link already ruled out fieldgemology.org hosts (those
            # come back as "wayback" above) — anything left is a genuine
            # external site, just needs to be absolute.
            try:
                return urljoin(base_url, href)
            except Exception:
                return href
        kind, target = res
        return f"#/page/{target}" if kind == "internal" else target

    def img_src_out(src, base_url, capture_ts):
        try:
            absu = urljoin(base_url, src)
        except Exception:
            absu = src
        return f"https://web.archive.org/web/{capture_ts}im_/{absu}" if capture_ts else absu

    # Nested "image wrapped in a link" markdown — e.g. a nav logo/thumbnail
    # linking to another page: [![alt](img.jpg)](target.php). The generic
    # LINK_RE below cannot parse this nesting (it matches the inner image
    # first and leaves the outer "](target.php)" as untouched literal text,
    # so the outer href never gets rewritten and stays a dead relative
    # path). Handle it explicitly, as raw HTML, before the generic pass.
    NESTED_RE = re.compile(r"\[!\[([^\]]*)\]\(((?:\\.|[^)])+?)\)\]\(((?:\\.|[^)])+?)\)")

    def rewrite_links_and_images(text, base_url, capture_ts, own_pid=None):
        def repl_nested(m):
            alt, imgsrc, linkhref = m.group(1), unescape_url(m.group(2)), unescape_url(m.group(3))
            href_out = resolve_href_out(linkhref, base_url, capture_ts, own_pid)
            src_out = img_src_out(imgsrc, base_url, capture_ts)
            alt_out = alt or os.path.basename(urlparse(src_out).path)
            target_attr = "" if href_out.startswith("#") else ' target="_blank" rel="noopener"'
            return (f'<a href="{html.escape(href_out)}"{target_attr}>'
                    f'<img class="photo" src="{html.escape(src_out)}" alt="{html.escape(alt_out)}"></a>')
        text = NESTED_RE.sub(repl_nested, text)

        # Angle-bracket autolinks — <http://...> — are a separate markdown
        # syntax from [label](url) and never touch LINK_RE below; without
        # this pass they fall through to Markdown's own autolink handling
        # completely unresolved, i.e. straight to the live domain.
        def repl_autolink(m):
            href = unescape_url(m.group(1))
            href_out = resolve_href_out(href, base_url, capture_ts, own_pid)
            if href_out.startswith("#"):
                return f"[{href}]({href_out})"
            return f'<a href="{html.escape(href_out)}" target="_blank" rel="noopener">{html.escape(href)}</a>'
        text = AUTOLINK_RE.sub(repl_autolink, text)

        def repl(m):
            bang, label, href = m.group(1), m.group(2), unescape_url(m.group(3))
            if bang == "!":
                src = img_src_out(href, base_url, capture_ts)
                alt = label or os.path.basename(urlparse(src).path)
                return f'<img class="photo" src="{html.escape(src)}" alt="{html.escape(alt)}">'
            href_out = resolve_href_out(href, base_url, capture_ts, own_pid)
            if href_out.startswith("#"):
                return f"[{label}]({href_out})"
            return f'<a href="{html.escape(href_out)}" target="_blank" rel="noopener">{label}</a>'
        return LINK_RE.sub(repl, text)

    def split_blocks(text):
        return [b for b in re.split(r"\n\s*\n", text.strip()) if b.strip()]

    freq = {}
    page_blocks = {}
    for pid, pg in pages.items():
        blocks = split_blocks(pg["body"])
        page_blocks[pid] = blocks
        seen = set()
        for b in blocks:
            norm = re.sub(r"\s+", " ", b).strip()
            if len(norm) < 30 or norm in seen:
                continue
            seen.add(norm)
            freq[norm] = freq.get(norm, 0) + 1

    CHROME_THRESHOLD = 8
    chrome_set = {norm for norm, c in freq.items() if c >= CHROME_THRESHOLD}
    print("distinct chrome blocks:", len(chrome_set), "/ distinct blocks:", len(freq))

    def is_chrome(b):
        return re.sub(r"\s+", " ", b).strip() in chrome_set

    GAP_TOL = 2

    def prefix_chrome_end(blocks):
        hits = [i for i, b in enumerate(blocks) if is_chrome(b)]
        if not hits or hits[0] > GAP_TOL:
            return 0
        last_chrome = hits[0]
        i = last_chrome + 1
        while i < len(blocks):
            if is_chrome(blocks[i]):
                last_chrome = i
                i += 1
            elif i - last_chrome <= GAP_TOL:
                i += 1
            else:
                break
        return last_chrome + 1

    def suffix_chrome_start(blocks):
        n = len(blocks)
        hits = [i for i, b in enumerate(blocks) if is_chrome(b)]
        if not hits or (n - 1 - hits[-1]) > GAP_TOL:
            return n
        last_chrome = hits[-1]
        i = last_chrome - 1
        while i >= 0:
            if is_chrome(blocks[i]):
                last_chrome = i
                i -= 1
            elif last_chrome - i <= GAP_TOL:
                i -= 1
            else:
                break
        return last_chrome

    md = mdlib.Markdown(extensions=["tables", "sane_lists"])

    def block_to_html(block, base_url, capture_ts, own_pid=None):
        md.reset()
        block = strip_stray_pipes(block)
        if not block.strip():
            return ""
        rewritten = rewrite_links_and_images(block, base_url, capture_ts, own_pid)
        try:
            return md.convert(rewritten)
        except Exception:
            return f"<pre>{rewritten}</pre>"

    chrome_html_cache = {}
    chrome_counter = [0]

    def get_chrome_id(norm_text, raw_block, base_url, capture_ts, own_pid):
        if norm_text not in chrome_html_cache:
            rendered = block_to_html(raw_block, base_url, capture_ts, own_pid)
            cid = f"c{chrome_counter[0]}"
            chrome_counter[0] += 1
            chrome_html_cache[norm_text] = (cid, rendered)
        return chrome_html_cache[norm_text][0]

    rendered_pages = {}
    for pid, pg in pages.items():
        blocks = page_blocks[pid]
        base_url = pg["source_url"]
        ts = pg["capture_date"].replace("-", "")
        pre_end = prefix_chrome_end(blocks)
        suf_start = suffix_chrome_start(blocks)
        if suf_start < pre_end:
            suf_start = len(blocks)

        segments = []
        if pre_end > 0:
            cids = [get_chrome_id(re.sub(r"\s+", " ", b).strip(), b, base_url, ts, pid) for b in blocks[:pre_end]]
            segments.append({"t": "c", "r": cids})
        for b in blocks[pre_end:suf_start]:
            segments.append({"t": "u", "h": block_to_html(b, base_url, ts, pid)})
        if suf_start < len(blocks):
            cids = [get_chrome_id(re.sub(r"\s+", " ", b).strip(), b, base_url, ts, pid) for b in blocks[suf_start:]]
            segments.append({"t": "c", "r": cids})

        rendered_pages[pid] = dict(
            title=pg["title"], source_url=pg["source_url"], capture_date=pg["capture_date"],
            wayback_snapshot=pg["wayback_snapshot"], site_era=pg["site_era"], category=pg["category"],
            relpath=pg["relpath"], segments=segments, raw=pg["body"],
        )

    chrome_blocks_out = {cid: html for (cid, html) in chrome_html_cache.values()}
    print("pages:", len(rendered_pages), "unique chrome blocks:", len(chrome_blocks_out))

    data = {"pages": rendered_pages, "chrome": chrome_blocks_out}
    raw = json.dumps(data, separators=(",", ":")).encode("utf-8")
    comp = gzip.compress(raw, compresslevel=9)
    data_b64 = base64.b64encode(comp).decode("ascii")
    print(f"data: {len(raw)} bytes raw -> {len(comp)} gzip -> {len(data_b64)} base64")

    fonts = fetch_fonts()
    template = open(os.path.join(SITE_DIR, "template.html"), encoding="utf-8").read()
    subs = {
        "__FONT_LORA_REGULAR__": fonts.get("Lora-Regular", ""),
        "__FONT_LORA_BOLD__": fonts.get("Lora-Bold", ""),
        "__FONT_WORKSANS_REGULAR__": fonts.get("WorkSans-Regular", ""),
        "__FONT_WORKSANS_SEMIBOLD__": fonts.get("WorkSans-SemiBold", ""),
        "__FONT_PLEXMONO_REGULAR__": fonts.get("IBMPlexMono-Regular", ""),
        "__DATA_B64__": data_b64,
    }
    for k, v in subs.items():
        template = template.replace(k, v)

    out_path = os.path.join(SITE_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(template)
    print("wrote", out_path, os.path.getsize(out_path), "bytes")

if __name__ == "__main__":
    build()
