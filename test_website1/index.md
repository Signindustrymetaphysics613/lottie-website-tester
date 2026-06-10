# test_website1 — Broken Links

A small fake news/blog site with intentionally broken internal and external
links sprinkled throughout. All other pages should be reachable.

## How to run

```sh
cd test_website1
../copy_lottie_to_test_folders.sh   # or run it once from the project root
python3 -m http.server 8001
# then open http://localhost:8001/lottie.html
```

## Site layout (15 pages, depth 3)

- `index.html` (depth 0)
- `about.html`, `contact.html`, `articles.html`, `archive.html` (depth 1)
- `article-1.html` through `article-9.html` (depth 2)
- `comments-article-1.html` (depth 3, linked from article-1)

## What Lottie should find

### Pages crawled successfully (15)
All 15 pages above should appear in the URL table with **HTTP 200**.

### Broken internal links (8 distinct missing URLs)
These are all `<a href="…">` targets pointing at files that don't exist.
Lottie should record each as **HTTP 404** and group them under the page that
linked to them.

| Missing URL                          | Linked from                  |
|--------------------------------------|------------------------------|
| `/missing-homepage-link.html`        | `index.html`                 |
| `/old-team-page.html`                | `about.html`                 |
| `/article-deleted.html`              | `articles.html`              |
| `/archive/old-1.html`                | `archive.html`               |
| `/archive/old-2.html`                | `archive.html`               |
| `/archive/old-3.html`                | `archive.html`               |
| `/404-test-page.html`                | `article-5.html`             |
| `/spam-comment-removed.html`         | `comments-article-1.html`    |

### Broken external links (2)
Fake/reserved domains that should fail to resolve. Lottie reports these as
network errors or opaque failures depending on browser behavior — the point
is that they should **not** appear as successful 200s.

| URL                                                          | Linked from        |
|--------------------------------------------------------------|--------------------|
| `https://example.invalid/support`                            | `contact.html`     |
| `https://this-domain-does-not-exist-2026.invalid/related`    | `article-2.html`   |

### Depth verification
- `comments-article-1.html` is only reachable via `index → articles → article-1 → comments-article-1`. If Lottie is run with `Max depth = 2`, this page should NOT be crawled.

### Notes
- No mixed content, no broken subresources, no redirects, no slow pages here — those are tested by other sites.
- No `robots.txt` — the whole site is crawlable.
