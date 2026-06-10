# test_website4 — Mixed Content

A fictional consulting site whose pages reference a mix of `http://` and
`https://` external resources. Tests Lottie's **Mixed Content** detector.

## How to run

```sh
cd test_website4
../copy_lottie_to_test_folders.sh
python3 -m http.server 8004
# then open http://localhost:8004/lottie.html
```

> ⚠️ **Important caveat.** "Mixed content" is specifically *insecure http://
> resources on a secure https:// page*. A plain `python3 -m http.server`
> serves over `http://`, so technically nothing is mixed and Lottie's
> Mixed Content tab may be empty.
>
> To exercise Lottie's mixed-content detection for real, serve this folder
> over HTTPS — for example with [`mkcert`](https://github.com/FiloSottile/mkcert) +
> a local TLS proxy like `caddy file-server`, or via a `localhost.run` /
> `ngrok` tunnel that terminates TLS. The HTML stays the same; only the
> origin scheme changes.
>
> Even over plain HTTP, every `http://...` reference below will still
> appear in Lottie's URL table — it just won't be flagged as **mixed
> content** unless the loading page is https.

## Site layout (15 pages, depth 2)

- `index.html` (depth 0)
- `about.html`, `services.html`, `case-studies.html` (depth 1)
- `case-studies/case-1.html` … `case-studies/case-11.html` (depth 2)

## What Lottie should find (when served over HTTPS)

### Pages crawled successfully (15)
All 15 pages return **HTTP 200**.

### Mixed content references (insecure `http://` on a secure page)

| Page                              | http:// resource(s)                                        |
|-----------------------------------|------------------------------------------------------------|
| `index.html`                      | `http://example.com/hero.jpg` (img)                        |
| `about.html`                      | `http://example.com/team.jpg` (img)                        |
| `services.html`                   | `http://example.com/icons.css` (stylesheet)                |
| `case-studies.html`               | `http://example.com/analytics.js` (script)                 |
| `case-studies/case-1.html`        | `http://example.com/case1.jpg` (img)                       |
| `case-studies/case-2.html`        | `http://example.com/case2.jpg` (img), `http://example.com/widget.js` (script) |
| `case-studies/case-3.html`        | `http://example.com/case3.jpg` (img)                       |
| `case-studies/case-4.html`        | `http://example.com/diagram.svg` (img)                     |
| `case-studies/case-5.html`        | `http://example.com/case5-style.css` (stylesheet)          |
| `case-studies/case-6.html`        | (none — control case, only https://)                       |
| `case-studies/case-7.html`        | `http://example.com/case7.jpg` (img)                       |
| `case-studies/case-8.html`        | `http://example.com/case8-tracker.js` (script)             |
| `case-studies/case-9.html`        | `http://example.com/case9.jpg`, `http://example.com/case9-style.css` |
| `case-studies/case-10.html`       | (none — control case, only https://)                       |
| `case-studies/case-11.html`       | `http://example.com/case11.jpg` (img)                      |

Total: **15 distinct `http://` resource URLs** spread across 13 pages.

### Secure reference (for contrast)
Every page also references `https://example.com/secure.css` so Lottie can
show that secure references don't trigger the mixed-content warning.

### Notes
- The `http://example.com/...` URLs will likely **fail to load** in
  practice (`example.com` exists, the paths don't), so they may also show
  up in Lottie's Errors tab as broken subresources. That's expected —
  whether Lottie flags them as *mixed content* is the feature being
  tested; whether they 404 is a side effect.
- No broken `<a>` links here. No redirects. No bloat.
