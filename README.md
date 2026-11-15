# Sanchez Consulting Services — website

Static, framework-free one-page site (Home · About · Services · Book · FAQ) + 404.
Booking and deposits run through the client's Acuity Scheduling account (https://sanchezconsulting.as.me/), embedded in the #book section; every service row deep-links to its Acuity appointment type.

## Rebuild
- `python3 tools/build_html.py` regenerates index.html, 404.html, sitemap.xml, robots.txt, site.webmanifest from the data at the top of the script (services, prices, FAQ, phone, domain).
  - `SITE=https://example.com` sets the canonical/OG/sitemap domain (default https://www.sanchezconsultingservices.com).
  - `BASE=/repo-name/` when hosting under a sub-path (e.g. a GitHub Pages project URL); default `/`.
- `python3 tools/build_images.py HERO.jpg ABOUT.jpg` rebuilds the portraits (WebP + JPG, 420/640/800w), logos, favicons and the 1200x630 OG image. The hero crop trims the bottom 10% (removes the sparkle watermark) and crops to 2:3; the about photo is cropped to 4:5.
  Without arguments it produces branded monogram placeholders.

## Client to supply / confirm (search the HTML for "PLACEHOLDER")
1. Portrait photos (hero + about) — then run build_images.py.
2. Domain: sanchezconsultingservices.com currently shows a Squarespace "Coming Soon" page — confirm it is hers.
3. Email address (footer), office hours, social links (Instagram/Facebook/Google Business Profile -> also add to JSON-LD "sameAs").
4. Credentials (PTIN/EA/AFSP etc.), years of experience, languages spoken, short personal bio line.
5. Testimonials — only real, client-approved quotes (template is commented out in index.html).
6. S-Corp price: Acuity lists $1,100 but its description says "Price begins at $800" — confirm which to show.
