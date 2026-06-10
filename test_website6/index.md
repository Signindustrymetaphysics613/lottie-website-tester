# test_website6 — Crawl Mechanics

A site whose purpose is to exercise Lottie's crawl-control settings:
`robots.txt`, max depth, max pages, and include/exclude patterns.

## How to run

```sh
cd test_website6
../copy_lottie_to_test_folders.sh
python3 -m http.server 8006
# then open http://localhost:8006/lottie.html
```

## Site layout (21 pages + `robots.txt`)

- `index.html` (depth 0)
- `about.html`, `sitemap.html` (depth 1)
- **Deep chain (depth 2 → 7):**
  - `content/level1/page.html` (depth 2)
  - `content/level1/level2/page.html` (depth 3)
  - `content/level1/level2/level3/page.html` (depth 4)
  - `content/level1/level2/level3/level4/page.html` (depth 5)
  - `content/level1/level2/level3/level4/level5/page.html` (depth 6)
  - `content/level1/level2/level3/level4/level5/level6/page.html` (depth 7)
- **Tag pages (depth 2, linked from sitemap):**
  - `tag/news.html`, `tag/code.html`, `tag/design.html`, `tag/lifestyle.html`, `tag/travel.html`
- **Category pages (depth 2, linked from sitemap):**
  - `category/cat-a.html`, `category/cat-b.html`, `category/cat-c.html`
- **Disallowed by robots.txt** (linked from sitemap so they *would* be found
  if Lottie weren't polite):
  - `secret/forbidden.html`
  - `secret/forbidden-2.html`
  - `admin/dashboard.html`
  - `admin/users.html`

## What Lottie should find

### With *default* "respect robots.txt" + generous depth/pages
- **17 pages crawled successfully** (HTTP 200):
  3 top-level + 6 deep + 5 tag + 3 category = 17.
- **4 pages skipped due to `robots.txt`:** the two `secret/` and the two
  `admin/` pages should appear flagged as "blocked by robots.txt" (or
  similar), not as 404s or 200s.

### With `robots.txt` ignored
All 21 pages crawl successfully (HTTP 200). The disallowed paths exist as
real files on disk.

### With `Max depth = 3`
Only depths 0–3 should be crawled. Expect:
- `index.html`, `about.html`, `sitemap.html` (depths 0–1)
- `content/level1/page.html` (depth 2)
- `content/level1/level2/page.html` (depth 3)
- All tag and category pages (depth 2)
- Levels 4, 5, 6, 7 of the deep chain are **NOT** crawled.

### With `Max pages = 10`
Lottie should stop after 10 pages (exact set depends on crawl order; the
test is that Lottie respects the cap and surfaces a "limit reached"
indicator).

### With include / exclude patterns
Suggested patterns to try:
- Exclude `^/tag/` → tag pages disappear from results.
- Exclude `level[3-9]` → the bottom of the deep chain is skipped.
- Include only `^/content/` → tag, category, about, sitemap all excluded.

### Notes
- No broken links, no broken subresources, no mixed content, no bloat
  here. The point is *what Lottie chooses to crawl*, not what it finds.
- The `robots.txt` is included in this folder. Lottie should fetch it
  before starting.
