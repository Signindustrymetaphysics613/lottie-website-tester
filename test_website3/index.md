# test_website3 — Broken Subresources

A fictional small site where every page is reachable (HTTP 200) but many
pages reference subresources — images, stylesheets, scripts — that are
missing. Tests Lottie's "Subresources" and "Errors" reports.

## How to run

```sh
cd test_website3
../copy_lottie_to_test_folders.sh
python3 -m http.server 8003
# then open http://localhost:8003/lottie.html
```

## Site layout (15 pages, depth 2)

- `index.html` (depth 0)
- `about.html`, `contact.html`, `products.html` (depth 1)
- `products/p1.html` … `products/p11.html` (depth 2)

Real files served by the static server:

- `styles.css` — a tiny working stylesheet (referenced by some pages so the
  passing case exists too)

## What Lottie should find

### Pages crawled successfully (15)
All 15 HTML pages return **HTTP 200** and contain no broken `<a href>` links.

### Broken subresources (each is a missing 404)

| Page                       | Missing subresource(s)                           |
|----------------------------|--------------------------------------------------|
| `index.html`               | `/img/hero-missing.png` (image)                  |
| `about.html`               | `/css/about-missing.css` (stylesheet)            |
| `contact.html`             | `/js/contact-missing.js` (script)                |
| `products.html`            | `/img/catalog-missing.png`, `/js/products-missing.js` |
| `products/p1.html`         | `/img/p1-missing.png`                            |
| `products/p2.html`         | `/img/p2-missing.png`                            |
| `products/p3.html`         | `/css/p3-missing.css`                            |
| `products/p4.html`         | `/js/p4-missing.js`                              |
| `products/p5.html`         | `/img/p5-missing.png`, `/css/p5-missing.css`, `/js/p5-missing.js` |
| `products/p6.html`         | (no missing subresources — control case)         |
| `products/p7.html`         | `/img/p7-missing.png`                            |
| `products/p8.html`         | `/css/p8-missing.css`                            |
| `products/p9.html`         | `/js/p9-missing.js`                              |
| `products/p10.html`        | `/img/p10-missing.png`, `/js/p10-missing.js`     |
| `products/p11.html`        | (no missing subresources — control case)         |

Total: **17 distinct missing subresource URLs**, referenced across 13 pages.

Lottie's "Errors" tab should group them by the page that requested them,
and the "Subresources" tab should break them down per page by type
(image / stylesheet / script).

### Working subresource
`styles.css` is referenced by `index.html` and a handful of product pages and
should load successfully — Lottie should show it once with HTTP 200 and the
list of pages that requested it.

### Notes
- No broken `<a>` links, no mixed content, no redirects — those are tested
  by other sites.
- `p6.html` and `p11.html` are deliberately clean control cases so Lottie's
  "no problems" rendering can be eyeballed.
