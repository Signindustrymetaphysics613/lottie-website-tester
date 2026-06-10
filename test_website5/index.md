# test_website5 — Redirects

A fictional site that uses `<meta http-equiv="refresh">` chains and JS
`window.location` redirects. Tests how Lottie treats client-side redirects
vs. genuine HTTP-level redirects.

## How to run

```sh
cd test_website5
../copy_lottie_to_test_folders.sh
python3 -m http.server 8005
# then open http://localhost:8005/lottie.html
```

> ⚠️ **Important caveat.** Lottie's "Redirects" / "redirect chain" feature
> is designed for *HTTP-level* 301/302/307/308 responses. A static
> `python3 -m http.server` cannot emit those — it always returns 200 with
> the file contents.
>
> This site therefore uses **client-side redirects** (`<meta refresh>` and
> JavaScript `window.location`). Lottie reads the HTML the server returns,
> so it will see these as ordinary pages with one outgoing link. Expect:
>
> - **No entries in the redirect-chain report** (no HTTP redirects exist).
> - Each "redirect" page appears in the URL table as a normal 200, and
>   the page it would redirect to appears as a separately-linked page.
> - JS-redirect destinations are still discovered *if* Lottie also follows
>   anchor tags on the page — this site puts a regular `<a href>` next to
>   the JS redirect so the destination is reachable either way.
>
> To actually test the HTTP-redirect feature, run a server that can emit
> 30x responses — e.g. a small Flask/Express app, or `caddy` with rewrite
> rules. Don't expect this folder to exercise the redirect-chain report
> on its own.

## Site layout (14 pages, depth 3)

- `index.html` (depth 0) — links to all chain starts
- `about.html`, `contact.html`, `normal-page.html` — plain pages (depth 1)
- **Chain A (3-hop meta-refresh):**
  - `chain-a-1.html` → `chain-a-2.html` → `chain-a-3.html` → `final-a.html`
- **Chain B (2-hop meta-refresh):**
  - `chain-b-1.html` → `chain-b-2.html` → `final-b.html`
- **Broken redirect:**
  - `chain-c-1.html` → `/missing-redirect-target.html` (404)
- **JS redirect:**
  - `js-redirect-1.html` → `js-final.html`

That's: 1 (index) + 3 (plain) + 4 (chain A) + 3 (chain B) + 1 (chain C) +
2 (JS) = **14 pages**.

## What Lottie should find

### Pages crawled successfully (14)
All 14 site pages return **HTTP 200**. Additionally:

- 1 broken URL: `/missing-redirect-target.html` (linked from
  `chain-c-1.html`'s meta refresh — whether Lottie discovers it depends on
  whether it parses meta-refresh URLs as links).

### Redirects
- **0** HTTP redirect chains (no server-side 30x responses possible from
  static server).

### Notes
- This site is a deliberate documentation of a limitation, not a
  positive-case test. The index.md is the test — it tells the user what
  Lottie *can't* detect here.
- For a real redirect-chain test, the user should set up a server that
  can issue 30x responses.
