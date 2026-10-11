# Aldawlia for Cooling Corporation website

Bilingual website (English, and Arabic right-to-left) for Aldawlia for Cooling Corporation
(المؤسسة الدولية للتبريد) and its family of companies: ERT, ETS, Nova Freeze, JET Solar, NEO Energy and GGG.
It also carries the brand guidelines. Version 1.1, October 2026, updated to the Group Presentation R4.0.

The site is static: plain HTML, CSS and a small script, generated from one bilingual content source.

## Repository layout

| Path | What it is |
|---|---|
| `docs/` | The built website, ready to serve. GitHub Pages publishes this folder. |
| `content/` | All text, as English/Arabic pairs: `T("English", "العربية")`. |
| `templates/` | Page layouts (Jinja2). |
| `static/` | `css/site.css` and `js/site.js`. |
| `build/` | Processed photos and 3D drawings, company logos, signature files, fonts and the map. Used as they are. |
| `deploy/` | Optional edge redirects for Cloudflare Pages and Netlify. |
| `tools/` | Scripts that produced `build/` from the original photos and company files (`tools/images.py` adds new photos). |
| `build.py` | The generator. |

## Pages

14 pages in each language, under `docs/en/` and `docs/ar/`: home, our story, the group, a page for each of
Aldawlia, JET Solar, ETS, Nova Freeze, NEO Energy and GGG, solutions, projects, sustainability, contact and
brand guidelines. `docs/index.html` is the language gateway.

## How the language is chosen

1. A language the visitor picked before (the language switch saves it) always wins.
2. With an edge redirect (Cloudflare or Netlify), the host's country lookup decides before the page loads.
3. Otherwise `index.html` decides in the browser from the device time zone; ambiguous zones fall back to the
   browser's region and language. Nothing is sent to a third party.

Arabic-speaking countries are the 22 Arab League members plus Western Sahara and Chad. Add `#ar` or `#en`
to the address to open either language directly.

## Editing and rebuilding

```bash
pip install jinja2 pillow
python3 build.py
```

This regenerates `docs/` (and `dist-artifact/`, a single-folder preview that is not committed). Commit the
updated `docs/` with the source change.

To add a photo, register it in `content/images.py` and run `python3 tools/images.py build/img`: it builds the
WebP sizes for new photos only and removes photos that are no longer registered. The 3D drawings with numbered
callouts are described in `content/figures.py`; marker positions are fractions of the image width and height.

## Publishing

- **GitHub Pages:** Settings › Pages › Build and deployment › Deploy from a branch › `main` and `/docs`.
  The site then runs at `https://shabrawyprime.github.io/aldawlia-website/`.
- **Custom domain:** add `www.aldawlia.org` under Settings › Pages › Custom domain and point the domain's
  DNS to GitHub Pages. Canonical, hreflang and sitemap URLs already use `https://www.aldawlia.org`.
- **Cloudflare Pages or Netlify:** publish `docs/`, and copy the matching folder from `deploy/` to get the
  language redirect at the edge.
- **Any other static host:** upload the contents of `docs/` as they are.

## Contact form

Without a form service the form prepares the enquiry for the visitor's email app and routes it to the right
company inbox. To receive submissions directly, set `FORM_ENDPOINT` in `build.py` to a form service URL
(Formspree, Basin or your own endpoint) and rebuild; the form then posts JSON to it.

© 2026 Aldawlia for Cooling Corporation. All rights reserved.
