# fieldgemology.org — recovered archive

`fieldgemology.org` was the field-expedition site of gemologist **Vincent
Pardieu** (later joined by Jean-Baptiste Senoble, Richard W. Hughes, and
others). From the mid-2000s it published first-hand expedition reports from
gem mining areas around the world — Kenya, Tanzania, Madagascar, Sri Lanka,
Myanmar, Cambodia, Vietnam, Laos, Afghanistan, Pakistan, Tajikistan, China,
Colombia, Mozambique — plus gemological studies (spinel, tsavorite,
tanzanite, Pamir ruby), a lab inclusion-photo database, and, from 2009
onward, a running expedition blog. The site was rebuilt on WordPress in
2017–2018, then went dark; by 2019 only login-probe traffic is captured.
The domain was later dropped and picked up by an unrelated party — captures
from 2023–2025 are parked-domain/app noise, not the original site, and are
**not** part of this archive.

This directory is a full-text recovery of the site, pulled from the
[Wayback Machine](https://web.archive.org/), organized by the site's four
distinct eras so the evolution is easy to follow. Every file carries a
front-matter block recording its original URL, the exact capture date, and
a link back to the live Wayback Machine snapshot, so any page here can be
traced back to its source and re-verified.

## Structure

```
archive/fieldgemology-org/
├── 00-homepage-timeline/          the front page over time: 2008, 2012, 2016 (blog era), 2018 (legacy old-fg. subdomain)
├── 01-original-site-2005-2009/    the original PHP site: expedition reports, articles, bio, links
│   ├── articles/                  the four flagship studies (spinel, tsavorite, tanzanite, Pamir ruby)
│   ├── expeditions/               ~40 country/region field-report pages
│   └── kenya-tsavo-mines-2009/    11 mine-by-mine reports from the Tsavo ruby/tsavorite belt
├── 02-blog-2009-2016/             the expedition blog: 42 individual posts + listing/gallery samples
├── 03-wordpress-relaunch-2017-2018/  the 2017-18 WordPress redesign's core pages
└── inventory.json                 machine-readable index: every file mapped to its source URL + timestamp
```

Each markdown file starts with:

```yaml
---
title: "..."
source_url: http://www.fieldgemology.org/...
capture_date: YYYY-MM-DD
wayback_snapshot: https://web.archive.org/web/TIMESTAMP/...
site_era: 01-original-site-2005-2009
---
```

Content below the front matter is the page's text converted to Markdown
(links and image references preserved) from the Wayback Machine's raw,
un-rewritten capture (the `id_` snapshot flag) — not summarized or
paraphrased. The site used a repeated table-based sidebar/nav on almost
every page in the 2005-2009 and 2009-2016 eras; that boilerplate is kept
intact as part of a faithful capture, with the page-specific content
following it.

## The site's four eras

### 1. Original site, 2005-2009 (`00-homepage-timeline/home-2008.md`, `01-original-site-2005-2009/`)

The earliest full crawl is **7 Jan 2008**. The homepage lists two big
trips — a 2005 Southeast-Asia/East-Africa circuit (Thailand, Burma, Laos,
Cambodia, Vietnam, Sri Lanka, Madagascar, Kenya, Tanzania) and a 2006
Central Asia trip (Pakistan, Afghanistan, Tajikistan, China) — each linking
out to per-country report pages. By 2009 the site had grown a second
generation of these reports (longer, more detailed URLs, e.g. the Kenya
Tsavo mine-by-mine series) sitting alongside the originals, a lab
inclusion-photo database (`LaboInclusion.php`), and the four articles later
reprinted by ICA's *InColor* and on ruby-sapphire.com. Author bio and site
links live in `Biography_FG03.php` / `Links.php`.

### 2. Blog era, 2009-2016 (`00-homepage-timeline/home-2012.md`, `02-blog-2009-2016/`)

Around 2009 the static report pages give way to a keyword-tagged blog
(`blog_display.php?key=...`). 42 distinct posts survive in the Wayback
Machine, tagged by place (Bangkok, Kashmir, Kenya, Pamir, Peshawar...),
material (ruby, sapphire, spinel, tsavorite, tanzanite, garnet, moonstone,
pearl...), or topic (treatment, conservation, research, GIA field reports).
Captures thin out sharply after 2013 and effectively stop after 2016 — the
site was updated less and less. A parallel `blog_byKey.php` tag-browsing
system (522 captured URL variants, one per keyword × crawl-date) is **not**
individually archived here since it's a listing view over the same 42
posts, not distinct content — see [Scope decisions](#scope-decisions).

### 3. WordPress relaunch, 2017-2018 (`03-wordpress-relaunch-2017-2018/`)

In 2017 the site was rebuilt on WordPress with a conventional
`/field-expeditions/`, `/articles-and-studies/`, `/news-and-conference/`
structure and topic-tag archive pages (`/tag/mozambique/`,
`/tag/tsavorite/`, etc.). The Wayback Machine only caught a handful of the
new long-form posts before the crawl trail runs out (Mozambique FE09,
Kenya FE09, Cambodia expeditions, Myanmar expeditions) — those and the
three section-index pages are what's archived here. No clean HTTP 200
capture of the new WordPress root homepage survives (only 301 redirects
through its `?p=NNNN` permalinks); `articles-and-studies-index.md`,
`field-expeditions-index.md`, and `news-and-conference-index.md` are the
closest thing to a front-page tour of this era. Tellingly, the relaunch
kept the entire 2005-2009 site alive underneath at `/OLD-FG/`, served from
the `old-fg.fieldgemology.org` subdomain, as a legacy fallback — same
content as era 1, so it isn't re-archived separately. That legacy subdomain
is what `00-homepage-timeline/home-2018.md` actually captures (there being
no surviving 200 for the real WordPress homepage at that date).

### 4. Death and domain drift, 2019-2025 (not archived)

The last real-site crawl is January 2018; 2019 only shows `wp-login.php`
probe traffic (bots checking for a live WordPress install), then nothing
until 2021 (one dead `blog_display.php` capture) and a scatter of 2023-2025
captures that are clearly a different, unrelated site occupying the
expired domain (`.well-known/openid-configuration`, `assetlinks.json`,
`ai-plugin.json` — app/API scaffolding, not gemology content). These are
excluded from the archive as noise.

## Scope decisions

The Wayback Machine holds **3,131** captured URLs for this domain across
its lifetime (2,806 of them HTTP 200s). Most of the volume is not
distinct content:

- **1,563 JPEGs** and other binary assets (photos) — not fetched; every
  markdown file below still shows the original `images/...` reference paths
  from the page, so photos can be re-fetched from the same Wayback
  snapshot (`https://web.archive.org/web/TIMESTAMP/ORIGINAL_URL`) if
  needed.
- **`LaboInclusionDetail.php`** (121 captures) and **`showpic.php`**
  (52 captures) are a lightbox-style single-photo viewer for the inclusion
  database and general photo galleries — one representative sample of each
  is archived (`laboratory-inclusion-detail-sample.md`,
  `photo-viewer-sample.md`); the rest are the same template around a
  different photo ID.
- **`blog_byKey.php` / `blog_byKey2.php`** (522 + 25 captures) are a
  tag-browse index over the same 42 blog posts already archived under
  `02-blog-2009-2016/posts/` — not fetched individually.
- **WordPress `/tag/*/` pages** (24 captures, 2017) are auto-generated
  listing pages, not distinct written content — not fetched; their topics
  match the tags already visible on the blog-era posts.
- **`/OLD-FG/*`** (2018) duplicates the original 2005-2009 site content
  already archived under `01-original-site-2005-2009/` — not re-fetched.
- Three duplicate blog-post filenames come from the same tag key captured
  with different capitalization (`congress`/`Congress`,
  `sapphire`/`Sapphire`, `Khao Ploy Waen`/`Khao ploy Waen`) — the later
  capture is kept.

The full raw capture list (all 3,131 rows, unfiltered) is preserved in
`cdx_full_index.json` for anyone who wants to go further — e.g. pull every
photo, every `LaboInclusionDetail.php` entry, or every dated blog-tag
snapshot.

## Full file inventory

### Homepage, across four snapshots (`00-homepage-timeline/`)

| Local file | Captured | Original URL |
|---|---|---|
| [`00-homepage-timeline/home-2008.md`](00-homepage-timeline/home-2008.md) | 2008-01-07 | http://www.fieldgemology.org:80/ |
| [`00-homepage-timeline/home-2012.md`](00-homepage-timeline/home-2012.md) | 2012-09-24 | http://www.fieldgemology.org/?p=2 |
| [`00-homepage-timeline/home-2016.md`](00-homepage-timeline/home-2016.md) | 2016-08-19 | http://fieldgemology.org/?p=3 |
| [`00-homepage-timeline/home-2018.md`](00-homepage-timeline/home-2018.md) | 2018-01-10 | http://old-fg.fieldgemology.org:80/ |

### Original site, 2005-2009 field reports (`01-original-site-2005-2009/`)

| Local file | Captured | Original URL |
|---|---|---|
| [`01-original-site-2005-2009/articles/pamirs-ruby-spinel-tajikistan.md`](01-original-site-2005-2009/articles/pamirs-ruby-spinel-tajikistan.md) | 2009-12-09 | http://www.fieldgemology.org:80/Pamirs_ruby_spinel_tajikistan.php |
| [`01-original-site-2005-2009/articles/spinel-article.md`](01-original-site-2005-2009/articles/spinel-article.md) | 2009-08-27 | http://www.fieldgemology.org:80/Spinel_article.php |
| [`01-original-site-2005-2009/articles/tanzanite-article.md`](01-original-site-2005-2009/articles/tanzanite-article.md) | 2009-10-29 | http://www.fieldgemology.org:80/Tanzanite_article.php |
| [`01-original-site-2005-2009/articles/tsavorite-article.md`](01-original-site-2005-2009/articles/tsavorite-article.md) | 2009-12-11 | http://www.fieldgemology.org:80/Tsavorite_article.php |
| [`01-original-site-2005-2009/biography-vincent-pardieu.md`](01-original-site-2005-2009/biography-vincent-pardieu.md) | 2009-12-09 | http://www.fieldgemology.org:80/Biography_FG03.php |
| [`01-original-site-2005-2009/category-link-index.md`](01-original-site-2005-2009/category-link-index.md) | 2008-01-10 | http://www.fieldgemology.org:80/cat_link.php |
| [`01-original-site-2005-2009/expeditions/afghanistan-ruby-jagdalek-emerald-panjshir.md`](01-original-site-2005-2009/expeditions/afghanistan-ruby-jagdalek-emerald-panjshir.md) | 2008-04-12 | http://www.fieldgemology.org:80/gemology%20afghanistan%20ruby%20jagdalek%20emerald%20panjshir.php |
| [`01-original-site-2005-2009/expeditions/burma-myanmar-legacy.md`](01-original-site-2005-2009/expeditions/burma-myanmar-legacy.md) | 2008-01-10 | http://www.fieldgemology.org:80/burmapage.php |
| [`01-original-site-2005-2009/expeditions/burma-myanmar-mergui-pearl-south-sea.md`](01-original-site-2005-2009/expeditions/burma-myanmar-mergui-pearl-south-sea.md) | 2008-04-12 | http://www.fieldgemology.org:80/Gemology%20burma%20myanmar%20mergui%20pearl%20south%20sea.php |
| [`01-original-site-2005-2009/expeditions/burma-myanmar-mogok-namya-monghsu-mergui-hpakant.md`](01-original-site-2005-2009/expeditions/burma-myanmar-mogok-namya-monghsu-mergui-hpakant.md) | 2008-04-17 | http://www.fieldgemology.org:80/gemology%20burma%20myanmar%20gemstone%20mogok%20namya%20mong%20hsu%20mergui%20hpakant.php |
| [`01-original-site-2005-2009/expeditions/cambodia-legacy.md`](01-original-site-2005-2009/expeditions/cambodia-legacy.md) | 2008-01-10 | http://www.fieldgemology.org:80/cambodiapage.php |
| [`01-original-site-2005-2009/expeditions/cambodia-pailin-sapphire-zircon-ratanakiri-ruby-samlot.md`](01-original-site-2005-2009/expeditions/cambodia-pailin-sapphire-zircon-ratanakiri-ruby-samlot.md) | 2008-04-17 | http://www.fieldgemology.org:80/gemology%20cambodia%20pailin%20sapphire%20zircon%20ratanakiri%20ruby%20samlot.php |
| [`01-original-site-2005-2009/expeditions/central-asia-00.md`](01-original-site-2005-2009/expeditions/central-asia-00.md) | 2008-01-10 | http://www.fieldgemology.org:80/central%20asia%2000.php |
| [`01-original-site-2005-2009/expeditions/central-asia-2006-overview.md`](01-original-site-2005-2009/expeditions/central-asia-2006-overview.md) | 2008-06-20 | http://www.fieldgemology.org:80/gemology%20central%20asia%202006.php |
| [`01-original-site-2005-2009/expeditions/central-asia-afghanistan.md`](01-original-site-2005-2009/expeditions/central-asia-afghanistan.md) | 2008-01-10 | http://www.fieldgemology.org:80/central%20asia%20afghanistan.php |
| [`01-original-site-2005-2009/expeditions/central-asia-pakistan.md`](01-original-site-2005-2009/expeditions/central-asia-pakistan.md) | 2008-01-10 | http://www.fieldgemology.org:80/central%20asia%20pakistan.php |
| [`01-original-site-2005-2009/expeditions/central-asia-tajikistan.md`](01-original-site-2005-2009/expeditions/central-asia-tajikistan.md) | 2008-01-10 | http://www.fieldgemology.org:80/central%20asia%20tajikistan.php |
| [`01-original-site-2005-2009/expeditions/china-emerald-davdar.md`](01-original-site-2005-2009/expeditions/china-emerald-davdar.md) | 2008-04-12 | http://www.fieldgemology.org:80/gemology%20china%20emerald%20davdar.php |
| [`01-original-site-2005-2009/expeditions/colombia-emerald.md`](01-original-site-2005-2009/expeditions/colombia-emerald.md) | 2008-04-12 | http://www.fieldgemology.org:80/gemology%20colombia%20emerald.php |
| [`01-original-site-2005-2009/expeditions/colombia-legacy.md`](01-original-site-2005-2009/expeditions/colombia-legacy.md) | 2008-01-10 | http://www.fieldgemology.org:80/colombia.php |
| [`01-original-site-2005-2009/expeditions/inclusion-gemstone-overview.md`](01-original-site-2005-2009/expeditions/inclusion-gemstone-overview.md) | 2008-04-17 | http://www.fieldgemology.org:80/gemology%20inclusion%20gem%20gemstone.php |
| [`01-original-site-2005-2009/expeditions/kenya-2005-overview.md`](01-original-site-2005-2009/expeditions/kenya-2005-overview.md) | 2008-04-12 | http://www.fieldgemology.org:80/gemology%20kenya%202005.php |
| [`01-original-site-2005-2009/expeditions/kenya-legacy.md`](01-original-site-2005-2009/expeditions/kenya-legacy.md) | 2008-01-10 | http://www.fieldgemology.org:80/kenyajuly2005.php |
| [`01-original-site-2005-2009/expeditions/kenya-ruby-tsavorite-tsavo-baringo-taita-mengare-kuranze-kasigau.md`](01-original-site-2005-2009/expeditions/kenya-ruby-tsavorite-tsavo-baringo-taita-mengare-kuranze-kasigau.md) | 2008-04-17 | http://www.fieldgemology.org:80/gemology%20kenya%20ruby%20tsavorite%20tsavo%20baringo%20taita%20mengare%20kuranze%20kasigau.php |
| [`01-original-site-2005-2009/expeditions/laos-legacy.md`](01-original-site-2005-2009/expeditions/laos-legacy.md) | 2008-01-10 | http://www.fieldgemology.org:80/laos.php |
| [`01-original-site-2005-2009/expeditions/laos-sapphire-houay-xai.md`](01-original-site-2005-2009/expeditions/laos-sapphire-houay-xai.md) | 2008-04-17 | http://www.fieldgemology.org:80/gemology%20laos%20sapphire%20houay%20xai.php |
| [`01-original-site-2005-2009/expeditions/madagascar-2005-overview.md`](01-original-site-2005-2009/expeditions/madagascar-2005-overview.md) | 2008-04-12 | http://www.fieldgemology.org:80/gemology%20madagascar%202005.php |
| [`01-original-site-2005-2009/expeditions/madagascar-ilakaka-andranondambo-ambondromifehy-vatomandry-andilamena.md`](01-original-site-2005-2009/expeditions/madagascar-ilakaka-andranondambo-ambondromifehy-vatomandry-andilamena.md) | 2008-04-17 | http://www.fieldgemology.org:80/gemology%20madagascar%20ruby%20sapphire%20ilakaka%20andranondambo%20ambondromifehy%20vatomandry%20andilamena.php |
| [`01-original-site-2005-2009/expeditions/madagascar-legacy.md`](01-original-site-2005-2009/expeditions/madagascar-legacy.md) | 2008-01-10 | http://www.fieldgemology.org:80/madajune2005.php |
| [`01-original-site-2005-2009/expeditions/painite.md`](01-original-site-2005-2009/expeditions/painite.md) | 2008-08-28 | http://www.fieldgemology.org/painite.php |
| [`01-original-site-2005-2009/expeditions/pakistan-ruby-emerald-kashmir-swat.md`](01-original-site-2005-2009/expeditions/pakistan-ruby-emerald-kashmir-swat.md) | 2008-04-12 | http://www.fieldgemology.org:80/gemology%20pakistan%20ruby%20emerald%20kashmir%20swat.php |
| [`01-original-site-2005-2009/expeditions/south-east-asia-summer-2005-overview.md`](01-original-site-2005-2009/expeditions/south-east-asia-summer-2005-overview.md) | 2008-04-12 | http://www.fieldgemology.org:80/gemology%20south%20east%20asia%20summer%202005.php |
| [`01-original-site-2005-2009/expeditions/sri-lanka-2005-overview.md`](01-original-site-2005-2009/expeditions/sri-lanka-2005-overview.md) | 2008-04-12 | http://www.fieldgemology.org:80/gemology%20sri%20lanka%20ceylon%202005.php |
| [`01-original-site-2005-2009/expeditions/sri-lanka-legacy.md`](01-original-site-2005-2009/expeditions/sri-lanka-legacy.md) | 2008-01-10 | http://www.fieldgemology.org:80/srilankamay2005.php |
| [`01-original-site-2005-2009/expeditions/sri-lanka-ratnapura-elahera-moonstone-metiyagoda-okkampitiya.md`](01-original-site-2005-2009/expeditions/sri-lanka-ratnapura-elahera-moonstone-metiyagoda-okkampitiya.md) | 2008-04-17 | http://www.fieldgemology.org:80/gemology%20sri%20lanka%20ceylon%20sapphire%20moonstone%20ratnapura%20elahera%20metiyagoda%20okkampitaya.php |
| [`01-original-site-2005-2009/expeditions/tajikistan-ruby-2011.md`](01-original-site-2005-2009/expeditions/tajikistan-ruby-2011.md) | 2011-05-09 | http://www.fieldgemology.org:80/gemology%20tajikistan%20ruby.php |
| [`01-original-site-2005-2009/expeditions/tajikistan-ruby-short.md`](01-original-site-2005-2009/expeditions/tajikistan-ruby-short.md) | 2008-08-28 | http://www.fieldgemology.org/ruby%20tajikistan.php |
| [`01-original-site-2005-2009/expeditions/tajikistan-ruby-spinel-pamir.md`](01-original-site-2005-2009/expeditions/tajikistan-ruby-spinel-pamir.md) | 2008-04-12 | http://www.fieldgemology.org:80/gemology%20tajikistan%20ruby%20spinel%20pamir.php |
| [`01-original-site-2005-2009/expeditions/tanzania-2005-overview.md`](01-original-site-2005-2009/expeditions/tanzania-2005-overview.md) | 2008-04-12 | http://www.fieldgemology.org:80/gemology%20tanzania%202005.php |
| [`01-original-site-2005-2009/expeditions/tanzania-dodoma-mpwapwa-winza.md`](01-original-site-2005-2009/expeditions/tanzania-dodoma-mpwapwa-winza.md) | 2009-02-16 | http://fieldgemology.org:80/Gemology%20tanzania%20ruby%20sapphire%20dodoma%20mpwapwa%20winza.php |
| [`01-original-site-2005-2009/expeditions/tanzania-legacy.md`](01-original-site-2005-2009/expeditions/tanzania-legacy.md) | 2008-01-10 | http://www.fieldgemology.org:80/tanzaniaaugust2005.php |
| [`01-original-site-2005-2009/expeditions/tanzania-tsavorite-alexandrite-merelani-lendanai-lemshuko-manyara.md`](01-original-site-2005-2009/expeditions/tanzania-tsavorite-alexandrite-merelani-lendanai-lemshuko-manyara.md) | 2008-08-28 | http://www.fieldgemology.org/gemology%20tanzania%20tsavorite%20alexandrite%20emerald%20tourmaline%20merelani%20lendanai%20lemshuko%20manyara.php |
| [`01-original-site-2005-2009/expeditions/tanzania-tunduru-songea-morogoro-merelani-umba.md`](01-original-site-2005-2009/expeditions/tanzania-tunduru-songea-morogoro-merelani-umba.md) | 2008-04-17 | http://www.fieldgemology.org:80/gemology%20tanzania%20ruby%20sapphire%20spinel%20tsavorite%20alexandrite%20emerald%20tunduru%20songea%20morogoro%20merelani%20umba.php |
| [`01-original-site-2005-2009/expeditions/tanzania-tunduru-songea-morogoro-merelani.md`](01-original-site-2005-2009/expeditions/tanzania-tunduru-songea-morogoro-merelani.md) | 2008-05-18 | http://www.fieldgemology.org:80/gemology%20tanzania%20ruby%20sapphire%20spinel%20tsavorite%20alexandrite%20emerald%20tunduru%20songea%20morogoro%20merelani.php |
| [`01-original-site-2005-2009/expeditions/travel-gem-market-mine-overview.md`](01-original-site-2005-2009/expeditions/travel-gem-market-mine-overview.md) | 2008-04-17 | http://www.fieldgemology.org:80/gemology%20travel%20gem%20gemstone%20market%20mine.php |
| [`01-original-site-2005-2009/expeditions/vietnam-2005-overview.md`](01-original-site-2005-2009/expeditions/vietnam-2005-overview.md) | 2008-04-12 | http://www.fieldgemology.org:80/gemology%20vietnam%202005.php |
| [`01-original-site-2005-2009/expeditions/vietnam-legacy.md`](01-original-site-2005-2009/expeditions/vietnam-legacy.md) | 2008-01-10 | http://www.fieldgemology.org:80/vietnamapr2005.php |
| [`01-original-site-2005-2009/expeditions/vietnam-luc-yen-quy-chau.md`](01-original-site-2005-2009/expeditions/vietnam-luc-yen-quy-chau.md) | 2008-04-17 | http://www.fieldgemology.org:80/gemology%20vietnam%20ruby%20spinel%20sapphire%20luc%20yen%20quy%20chau.php |
| [`01-original-site-2005-2009/ica-2000-presentation.md`](01-original-site-2005-2009/ica-2000-presentation.md) | 2008-01-10 | http://www.fieldgemology.org:80/ICA00.php |
| [`01-original-site-2005-2009/kenya-tsavo-mines-2009/baringo-ruby-corby.md`](01-original-site-2005-2009/kenya-tsavo-mines-2009/baringo-ruby-corby.md) | 2009-12-10 | http://www.fieldgemology.org:80/Gemology%20kenya%20baringo%20ruby%20corby.php |
| [`01-original-site-2005-2009/kenya-tsavo-mines-2009/ruby-aqua.md`](01-original-site-2005-2009/kenya-tsavo-mines-2009/ruby-aqua.md) | 2009-10-05 | http://www.fieldgemology.org:80/Gemology%20kenya%20tsavo%20ruby%20aqua.php |
| [`01-original-site-2005-2009/kenya-tsavo-mines-2009/ruby-equator.md`](01-original-site-2005-2009/kenya-tsavo-mines-2009/ruby-equator.md) | 2009-12-10 | http://www.fieldgemology.org:80/Gemology%20kenya%20tsavo%20ruby%20equator.php |
| [`01-original-site-2005-2009/kenya-tsavo-mines-2009/ruby-hardrock.md`](01-original-site-2005-2009/kenya-tsavo-mines-2009/ruby-hardrock.md) | 2009-12-10 | http://www.fieldgemology.org:80/Gemology%20kenya%20tsavo%20ruby%20hardrock.php |
| [`01-original-site-2005-2009/kenya-tsavo-mines-2009/ruby-rockland.md`](01-original-site-2005-2009/kenya-tsavo-mines-2009/ruby-rockland.md) | 2009-12-09 | http://www.fieldgemology.org:80/Gemology%20kenya%20tsavo%20ruby%20rockland.php |
| [`01-original-site-2005-2009/kenya-tsavo-mines-2009/ruby-simba.md`](01-original-site-2005-2009/kenya-tsavo-mines-2009/ruby-simba.md) | 2009-12-10 | http://www.fieldgemology.org:80/Gemology%20kenya%20ruby%20simba.php |
| [`01-original-site-2005-2009/kenya-tsavo-mines-2009/tsavo-garnet.md`](01-original-site-2005-2009/kenya-tsavo-mines-2009/tsavo-garnet.md) | 2009-12-10 | http://www.fieldgemology.org:80/Gemology%20kenya%20tsavo%20garnet.php |
| [`01-original-site-2005-2009/kenya-tsavo-mines-2009/tsavorite-baraka.md`](01-original-site-2005-2009/kenya-tsavo-mines-2009/tsavorite-baraka.md) | 2009-12-19 | http://www.fieldgemology.org:80/Gemology%20kenya%20tsavo%20tsavorite%20baraka.php |
| [`01-original-site-2005-2009/kenya-tsavo-mines-2009/tsavorite-bocrest.md`](01-original-site-2005-2009/kenya-tsavo-mines-2009/tsavorite-bocrest.md) | 2009-12-10 | http://www.fieldgemology.org:80/Gemology%20kenya%20tsavo%20tsavorite%20bocrest.php |
| [`01-original-site-2005-2009/kenya-tsavo-mines-2009/tsavorite-bridges.md`](01-original-site-2005-2009/kenya-tsavo-mines-2009/tsavorite-bridges.md) | 2009-12-10 | http://www.fieldgemology.org:80/Gemology%20kenya%20tsavo%20tsavorite%20bridges.php |
| [`01-original-site-2005-2009/kenya-tsavo-mines-2009/tsavorite-nadan-kuranze.md`](01-original-site-2005-2009/kenya-tsavo-mines-2009/tsavorite-nadan-kuranze.md) | 2009-12-10 | http://www.fieldgemology.org:80/Gemology%20kenya%20tsavo%20kuranze%20tsavorite%20nadan.php |
| [`01-original-site-2005-2009/kenya-tsavo-mines-2009/tsavorite-travolite.md`](01-original-site-2005-2009/kenya-tsavo-mines-2009/tsavorite-travolite.md) | 2009-12-10 | http://www.fieldgemology.org:80/Gemology%20kenya%20tsavo%20tsavorite%20travolite.php |
| [`01-original-site-2005-2009/laboratory-inclusion-database.md`](01-original-site-2005-2009/laboratory-inclusion-database.md) | 2009-01-22 | http://www.fieldgemology.org:80/LaboInclusion.php |
| [`01-original-site-2005-2009/laboratory-inclusion-detail-sample.md`](01-original-site-2005-2009/laboratory-inclusion-detail-sample.md) | 2008-01-10 | http://www.fieldgemology.org:80/LaboInclusionDetail.php?type=lab&id=206&sub_id=44 |
| [`01-original-site-2005-2009/links.md`](01-original-site-2005-2009/links.md) | 2008-04-21 | http://www.fieldgemology.org:80/Links.php?cat_id=3 |
| [`01-original-site-2005-2009/newsletter-01.md`](01-original-site-2005-2009/newsletter-01.md) | 2008-04-17 | http://www.fieldgemology.org:80/newsletter/file/fieldgemologynewsletter01.htm |
| [`01-original-site-2005-2009/photo-viewer-sample.md`](01-original-site-2005-2009/photo-viewer-sample.md) | 2008-03-24 | http://www.fieldgemology.org:80/showpic.php?sub_id=&type= |
| [`01-original-site-2005-2009/summer-2005-ica-aigs-gubelin-presentation.md`](01-original-site-2005-2009/summer-2005-ica-aigs-gubelin-presentation.md) | 2008-06-20 | http://www.fieldgemology.org:80/Summer%202005%20ICA%20AIGS%20Gubelin%20presentation.php |

### Blog era, 2009-2016 (`02-blog-2009-2016/`)

| Local file | Captured | Original URL |
|---|---|---|
| [`02-blog-2009-2016/blog-gallery-sample.md`](02-blog-2009-2016/blog-gallery-sample.md) | 2010-10-27 | http://www.fieldgemology.org:80/blog_gallery.php |
| [`02-blog-2009-2016/blog-gallery2-sample.md`](02-blog-2009-2016/blog-gallery2-sample.md) | 2010-10-26 | http://www.fieldgemology.org:80/blog_gallery2.php? |
| [`02-blog-2009-2016/blog-gallery3-sample.md`](02-blog-2009-2016/blog-gallery3-sample.md) | 2010-10-26 | http://www.fieldgemology.org:80/blog_gallery3.php? |
| [`02-blog-2009-2016/blog-homepage-listing.md`](02-blog-2009-2016/blog-homepage-listing.md) | 2009-10-05 | http://fieldgemology.org:80/blog_display.php? |
| [`02-blog-2009-2016/mozambique-expedition-fe09-part01.md`](02-blog-2009-2016/mozambique-expedition-fe09-part01.md) | 2012-09-20 | http://www.fieldgemology.org/blog_FE09_Mozambique_Part01.htm |
| [`02-blog-2009-2016/posts/award.md`](02-blog-2009-2016/posts/award.md) | 2012-09-19 | http://www.fieldgemology.org/blog_display.php?id=43&key=award |
| [`02-blog-2009-2016/posts/badakshan.md`](02-blog-2009-2016/posts/badakshan.md) | 2012-09-24 | http://www.fieldgemology.org/blog_display.php?id=61&key=Badakshan |
| [`02-blog-2009-2016/posts/bangkok.md`](02-blog-2009-2016/posts/bangkok.md) | 2016-08-19 | http://fieldgemology.org/blog_display.php?id=1&key=Bangkok |
| [`02-blog-2009-2016/posts/black-star-sapphire.md`](02-blog-2009-2016/posts/black-star-sapphire.md) | 2011-09-27 | http://www.fieldgemology.org/blog_display.php?id=24&key=black%20star%20sapphire |
| [`02-blog-2009-2016/posts/bridges.md`](02-blog-2009-2016/posts/bridges.md) | 2016-08-19 | http://fieldgemology.org/blog_display.php?id=78&key=Bridges |
| [`02-blog-2009-2016/posts/china.md`](02-blog-2009-2016/posts/china.md) | 2012-09-24 | http://www.fieldgemology.org/blog_display.php?id=87&key=China |
| [`02-blog-2009-2016/posts/congress.md`](02-blog-2009-2016/posts/congress.md) | 2015-02-25 | http://www.fieldgemology.org/blog_display.php?id=27&key=Congress |
| [`02-blog-2009-2016/posts/conservation.md`](02-blog-2009-2016/posts/conservation.md) | 2012-09-17 | http://www.fieldgemology.org/blog_display.php?id=56&key=conservation |
| [`02-blog-2009-2016/posts/davdar.md`](02-blog-2009-2016/posts/davdar.md) | 2016-08-19 | http://fieldgemology.org/blog_display.php?id=73&key=Davdar |
| [`02-blog-2009-2016/posts/emerald.md`](02-blog-2009-2016/posts/emerald.md) | 2011-08-28 | http://www.fieldgemology.org/blog_display.php?id=57&key=emerald |
| [`02-blog-2009-2016/posts/field-report-gia.md`](02-blog-2009-2016/posts/field-report-gia.md) | 2012-09-22 | http://www.fieldgemology.org/blog_display.php?id=58&key=Field%20Report%20GIA |
| [`02-blog-2009-2016/posts/garnet.md`](02-blog-2009-2016/posts/garnet.md) | 2012-09-25 | http://www.fieldgemology.org/blog_display.php?id=55&key=garnet |
| [`02-blog-2009-2016/posts/glass.md`](02-blog-2009-2016/posts/glass.md) | 2012-09-19 | http://www.fieldgemology.org/blog_display.php?id=45&key=glass |
| [`02-blog-2009-2016/posts/gogogogo.md`](02-blog-2009-2016/posts/gogogogo.md) | 2016-08-19 | http://fieldgemology.org/blog_display.php?id=31&key=Gogogogo |
| [`02-blog-2009-2016/posts/hughes.md`](02-blog-2009-2016/posts/hughes.md) | 2016-08-19 | http://fieldgemology.org/blog_display.php?id=53&key=Hughes |
| [`02-blog-2009-2016/posts/kaghan.md`](02-blog-2009-2016/posts/kaghan.md) | 2012-09-20 | http://www.fieldgemology.org/blog_display.php?id=59&key=Kaghan |
| [`02-blog-2009-2016/posts/kashmir.md`](02-blog-2009-2016/posts/kashmir.md) | 2016-08-19 | http://fieldgemology.org/blog_display.php?id=26&key=Kashmir |
| [`02-blog-2009-2016/posts/kenya.md`](02-blog-2009-2016/posts/kenya.md) | 2011-08-31 | http://www.fieldgemology.org/blog_display.php?id=36&key=Kenya |
| [`02-blog-2009-2016/posts/khao-ploy-waen.md`](02-blog-2009-2016/posts/khao-ploy-waen.md) | 2016-08-19 | http://fieldgemology.org/blog_display.php?id=21&key=Khao%20Ploy%20Waen |
| [`02-blog-2009-2016/posts/mavuco.md`](02-blog-2009-2016/posts/mavuco.md) | 2012-09-25 | http://www.fieldgemology.org/blog_display.php?id=38&key=Mavuco |
| [`02-blog-2009-2016/posts/mjp.md`](02-blog-2009-2016/posts/mjp.md) | 2012-09-24 | http://www.fieldgemology.org/blog_display.php?id=51&key=MJP |
| [`02-blog-2009-2016/posts/moonstone.md`](02-blog-2009-2016/posts/moonstone.md) | 2016-08-19 | http://fieldgemology.org/blog_display.php?id=76&key=moonstone |
| [`02-blog-2009-2016/posts/niassa.md`](02-blog-2009-2016/posts/niassa.md) | 2012-09-22 | http://www.fieldgemology.org/blog_display.php?id=42&key=Niassa |
| [`02-blog-2009-2016/posts/pailin.md`](02-blog-2009-2016/posts/pailin.md) | 2012-09-25 | http://www.fieldgemology.org/blog_display.php?id=82&key=Pailin |
| [`02-blog-2009-2016/posts/pamir.md`](02-blog-2009-2016/posts/pamir.md) | 2016-08-19 | http://fieldgemology.org/blog_display.php?id=72&key=Pamir |
| [`02-blog-2009-2016/posts/pearl-farm.md`](02-blog-2009-2016/posts/pearl-farm.md) | 2011-08-31 | http://www.fieldgemology.org/blog_display.php?id=54&key=pearl%20farm |
| [`02-blog-2009-2016/posts/peshawar.md`](02-blog-2009-2016/posts/peshawar.md) | 2016-08-19 | http://fieldgemology.org/blog_display.php?id=70&key=Peshawar |
| [`02-blog-2009-2016/posts/quy-chau.md`](02-blog-2009-2016/posts/quy-chau.md) | 2016-08-19 | http://fieldgemology.org/blog_display.php?id=75&key=Quy%20Chau |
| [`02-blog-2009-2016/posts/richard-wise.md`](02-blog-2009-2016/posts/richard-wise.md) | 2012-09-14 | http://www.fieldgemology.org/blog_display.php?id=49&key=Richard%20Wise |
| [`02-blog-2009-2016/posts/ruby.md`](02-blog-2009-2016/posts/ruby.md) | 2012-09-17 | http://www.fieldgemology.org/blog_display.php?id=44&key=ruby |
| [`02-blog-2009-2016/posts/sapphire.md`](02-blog-2009-2016/posts/sapphire.md) | 2013-05-30 | http://www.fieldgemology.org/blog_display.php?id=90&key=Sapphire |
| [`02-blog-2009-2016/posts/spinel.md`](02-blog-2009-2016/posts/spinel.md) | 2012-11-02 | http://www.fieldgemology.org/blog_display.php?id=86&key=spinel |
| [`02-blog-2009-2016/posts/studies.md`](02-blog-2009-2016/posts/studies.md) | 2012-09-24 | http://www.fieldgemology.org/blog_display.php?id=81&key=studies |
| [`02-blog-2009-2016/posts/taita.md`](02-blog-2009-2016/posts/taita.md) | 2016-08-19 | http://fieldgemology.org/blog_display.php?id=34&key=Taita |
| [`02-blog-2009-2016/posts/tanzania.md`](02-blog-2009-2016/posts/tanzania.md) | 2016-08-19 | http://fieldgemology.org/blog_display.php?id=62&key=Tanzania |
| [`02-blog-2009-2016/posts/tanzanite.md`](02-blog-2009-2016/posts/tanzanite.md) | 2012-09-24 | http://www.fieldgemology.org/blog_display.php?id=35&key=tanzanite |
| [`02-blog-2009-2016/posts/treatment.md`](02-blog-2009-2016/posts/treatment.md) | 2012-09-22 | http://www.fieldgemology.org/blog_display.php?id=47&key=treatment |
| [`02-blog-2009-2016/posts/tsavorite.md`](02-blog-2009-2016/posts/tsavorite.md) | 2012-09-19 | http://www.fieldgemology.org/blog_display.php?id=85&key=tsavorite |
| [`02-blog-2009-2016/posts/winza.md`](02-blog-2009-2016/posts/winza.md) | 2012-09-25 | http://www.fieldgemology.org/blog_display.php?id=39&key=Winza |

### WordPress relaunch, 2017-2018 (`03-wordpress-relaunch-2017-2018/`)

| Local file | Captured | Original URL |
|---|---|---|
| [`03-wordpress-relaunch-2017-2018/articles-and-studies-index.md`](03-wordpress-relaunch-2017-2018/articles-and-studies-index.md) | 2017-08-19 | http://fieldgemology.org:80/articles-and-studies/ |
| [`03-wordpress-relaunch-2017-2018/expeditions-to-cambodia.md`](03-wordpress-relaunch-2017-2018/expeditions-to-cambodia.md) | 2017-08-19 | http://fieldgemology.org:80/field-expeditions/asia/expeditions-to-cambodia/ |
| [`03-wordpress-relaunch-2017-2018/expeditions-to-myanmar.md`](03-wordpress-relaunch-2017-2018/expeditions-to-myanmar.md) | 2017-08-18 | http://fieldgemology.org:80/expeditions-to-myanmar/ |
| [`03-wordpress-relaunch-2017-2018/fe09-northern-mozambique.md`](03-wordpress-relaunch-2017-2018/fe09-northern-mozambique.md) | 2017-08-23 | http://fieldgemology.org:80/fe09-northern-mozambique/ |
| [`03-wordpress-relaunch-2017-2018/fe09-part-06-kenya.md`](03-wordpress-relaunch-2017-2018/fe09-part-06-kenya.md) | 2017-08-23 | http://fieldgemology.org:80/fe09-part-06-kenya/ |
| [`03-wordpress-relaunch-2017-2018/fe09-part-7-to-mozambique.md`](03-wordpress-relaunch-2017-2018/fe09-part-7-to-mozambique.md) | 2017-08-24 | http://fieldgemology.org:80/fe09-part-7-to-mozambique/ |
| [`03-wordpress-relaunch-2017-2018/news-and-conference-index.md`](03-wordpress-relaunch-2017-2018/news-and-conference-index.md) | 2017-08-23 | http://fieldgemology.org:80/news-and-conference/ |
