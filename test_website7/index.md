# test_website7 — Kitchen Sink ("Wren & Iron")

A fictional small kitchen-goods shop that mixes **all** of the issues
exercised by test_website1–6 into one realistic-looking site. This is the
end-to-end smoke test for Lottie: every report tab should have something
in it after crawling this site.

## How to run

```sh
cd test_website7
../copy_lottie_to_test_folders.sh
python3 -m http.server 8007
# then open http://localhost:8007/lottie.html
```

## Site layout (~25 pages, depth 3)

- `index.html` — home
- `about.html`, `shop.html`, `blog.html`, `contact.html`, `shipping.html`,
  `returns.html`, `faq.html`, `locations.html`, `newsletter.html`,
  `press.html` — top-level (depth 1)
- `shop/<slug>.html` — 8 product pages (depth 2)
- `blog/<slug>.html` — 4 blog posts (depth 2)
- `old-shop.html` — a meta-refresh redirect to `/shop.html` (legacy URL)

Plus subresources: `styles.css`, `hero.svg`, `large-product.svg`.

## What Lottie should find

### Broken links (test_website1 features)
| Missing URL                              | Linked from              |
|------------------------------------------|--------------------------|
| `/shop/cast-iron-press.html` (404)       | `shop.html`              |
| `/legacy-blog-post.html` (404)           | `blog.html`              |
| `https://example.invalid/wholesale`      | `press.html` (external)  |

### Page bloat (test_website2 features)
- `shop/dutch-oven.html` is heavy — large inline SVG (~80 KB).
- `shop/skillet.html` references `large-product.svg` (~500 KB).
- All other pages are 1–5 KB.

Top 2 in "Heaviest 10": `shop/skillet.html` (with the SVG subresource) and
`shop/dutch-oven.html`.

### Broken subresources (test_website3 features)
| Page                       | Missing subresource                |
|----------------------------|------------------------------------|
| `index.html`               | `/img/missing-hero-bg.png`         |
| `about.html`               | `/img/missing-team-photo.jpg`      |
| `shop/wooden-spoon.html`   | `/css/wooden-spoon-missing.css`    |
| `faq.html`                 | `/js/faq-search-missing.js`        |

### Mixed content (test_website4 features)
*(Only flagged if served over HTTPS; see test_website4/index.md.)*

| Page                       | Insecure resource                            |
|----------------------------|----------------------------------------------|
| `locations.html`           | `http://example.com/map-tiles.png`           |
| `newsletter.html`          | `http://example.com/subscribe-widget.js`     |
| `blog/recipes.html`        | `http://example.com/share-button.css`        |

### Redirects (test_website5 features — client-side only)
- `old-shop.html` uses `<meta http-equiv="refresh">` to send the browser to
  `/shop.html`. Lottie sees it as a normal 200 page; the real
  redirect-chain feature still needs a server that can emit 30x.

### Crawl mechanics (test_website6 features)
- No `robots.txt` here (this is the "real site" simulation; everything
  should be crawlable).
- Maximum depth is 3 (`index → shop → product-page` and `index → blog →
  post`).

### Summary of what each Lottie tab should show
- **All URLs**: ~25 pages + a few SVG/CSS subresources + ~7 broken URLs.
- **Errors**: ~7 broken URLs grouped by linking page.
- **Subresources**: per-page breakdown of imgs/css/js, including misses.
- **Mixed content**: empty over http://, populated over https://.
- **Heaviest 10**: `skillet`, `dutch-oven`, then the rest.
- **Slowest 10**: not meaningfully exercised (static server, all sub-ms
  responses).
