#!/usr/bin/env python3
"""Generates index.html and 404.html. Edit SITE / SERVICES / FAQ below, then run: python3 tools/build_html.py"""
import json, os, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.environ.get("SITE", "https://www.sanchezconsultingservices.com")   # canonical domain (see README)
BASE = os.environ.get("BASE", "/")   # "/" for a custom domain; "/repo-name/" for a GitHub Pages project URL
BOOK = "https://sanchezconsulting.as.me/"
EMBED = "https://app.acuityscheduling.com/schedule/0b03b2fb?ref=embedded_csp"
PHONE_DISPLAY, PHONE_TEL = "(415) 200-7148", "+14152007148"
OWNER = "Telma Sanchez Perez"
DEPOSIT = "A non-refundable deposit is required to reserve your appointment. Deposits are applied toward your tax preparation fee."

PREP = [
 (87189138, "Individual Tax Return — W-2 Only", "For W-2 income only, with standard deductions and credits. One individual return.", "400", True, 90, ["W-2", "Single filer"]),
 (87189154, "Married Filing Jointly — W-2 Only", "Married filing jointly with W-2 income and/or unemployment (1099-G) only — one return for two adults. Does not include 1099-NEC income.", "600", False, 120, ["W-2", "1099-G", "Joint return"]),
 (87189214, "W-2 + Side Job / Sole Proprietor", "Your W-2 income plus a side business or sole proprietorship, filing single or married jointly. Annual business expense totals by category are required.", "700", False, 150, ["Schedule C", "Self-employed"]),
 (87201214, "LLC + Personal Tax Return", "Your LLC business return together with your personal return (Schedule C, Form 1040 and related schedules). Pricing begins here and may increase with complexity — any additional fees are discussed beforehand.", "800", True, 180, ["LLC", "Form 1040"]),
 (87203194, "S-Corporation Tax Return", "Form 1120-S S-Corporation return with owner K-1s. Pricing varies by activity and records, and any additional fees are discussed beforehand.", "1,100", True, 180, ["Form 1120-S", "K-1s"]),
 (88546451, "Tax Return Amendment", "Prior-year corrections and adjustments. A full review of your originally filed return and a recalculation of your tax liability based on corrected information. Returns can be amended for up to three prior years.", "600", False, 150, ["Prior years", "Corrections"]),
]
ADVISORY = [
 (87188940, "Tax Strategy Consultation", "A focused, private session for tax strategy and planning, IRS and FTB notices, and return review. Meet by phone, Zoom, FaceTime or in person in San Francisco. Please bring any documents you would like to discuss.", "197", False, 50, ["Planning", "IRS & FTB notices", "Return review"]),
 (87465286, "Quick Tax Question", "For one or two targeted questions — withholding and W-4, filing status, a specific notice, or a focused “what should I do next?”. Consultation only; does not include tax preparation or filing.", "95", False, 20, ["Quick guidance"]),
]
FAQ = [
 ("Which appointment should I book?", f"Choose the appointment that matches your return. Not sure which one fits? Text <a href=\"sms:{PHONE_TEL}\">{PHONE_DISPLAY}</a> and Telma will schedule you."),
 ("Do married couples need one appointment or two?", "Each appointment covers one tax return. Married filing jointly is one return for both spouses, so one appointment. Two single people filing separately need two appointments."),
 ("Is a deposit required, and how is it used?", "Yes. A non-refundable deposit is taken through the online scheduler when you book, and it is applied toward your tax preparation fee. Consultations and Quick Tax Questions are paid in full at booking."),
 ("What is the cancellation and rescheduling policy?", "Please give at least 24 hours’ notice to reschedule. Appointments canceled or rescheduled with less than 24 hours’ notice, or missed without notice, forfeit the deposit. For consultations, payment may be transferred one time to a new appointment with 24 hours’ notice."),
 ("Where is the office?", f"The office is in San Francisco. The address is provided after your appointment is confirmed — please text <a href=\"sms:{PHONE_TEL}\">{PHONE_DISPLAY}</a> before your appointment to receive location details."),
 ("Can I meet remotely?", "Tax Strategy Consultations and Quick Tax Questions can be held by phone, Zoom, FaceTime, or in person in San Francisco — you choose when you book."),
 ("What should self-employed and business clients bring?", "Annual totals by category for income and business expenses, rather than individual receipts, plus vehicle mileage and home-office figures if they apply. Keep your receipts and records for your own files."),
 ("How far back can a return be amended?", "Amendments can be prepared for up to three prior tax years."),
]

ARROW = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M1 8h13M9 3l5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>'

def svc_rows(items, start):
    out = []
    for i, (aid, name, desc, price, frm, dur, tags) in enumerate(items):
        d = f"{dur // 60} hr {dur % 60} min" if dur >= 60 and dur % 60 else (f"{dur // 60} hr" if dur >= 60 else f"{dur} min")
        d = d.replace("1 hr 30 min", "90 min").replace("2 hr 30 min", "2.5 hrs").replace("2 hr", "2 hrs").replace("3 hr", "3 hrs")
        tg = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in tags)
        out.append(f'''        <li class="svc reveal">
          <span class="idx">{start + i:02d}</span>
          <div>
            <h4>{html.escape(name)}</h4>
            <p>{html.escape(desc)}</p>
            <div class="tags">{tg}</div>
          </div>
          <div class="price">
            <small>{"Starting at" if frm else "Fee"}</small>
            <strong class="gold-text">${price}</strong>
            <span class="dur">{d} appointment</span>
            <a class="book-link" href="{BOOK}?appointmentType={aid}" target="_blank" rel="noopener" aria-label="Book {html.escape(name)} (opens scheduler)">Book this</a>
          </div>
        </li>''')
    return "\n".join(out)

def offers(items):
    return [{"@type": "Offer", "price": p.replace(",", ""), "priceCurrency": "USD", "url": f"{BOOK}?appointmentType={a}",
             "itemOffered": {"@type": "Service", "name": n, "description": d}} for a, n, d, p, f, dur, t in items]

ld = {"@context": "https://schema.org", "@graph": [
  {"@type": ["AccountingService", "ProfessionalService"], "@id": f"{SITE}/#business", "name": "Sanchez Consulting Services",
   "legalName": "Sanchez Consulting Services LLC", "url": f"{SITE}/", "logo": f"{SITE}/assets/img/logo-stacked.png",
   "image": f"{SITE}/assets/img/og-image.jpg", "telephone": PHONE_TEL,
   "description": "Tax preparation and tax strategy in San Francisco for individuals, married couples, the self-employed, LLCs and S-Corporations.",
   "address": {"@type": "PostalAddress", "addressLocality": "San Francisco", "addressRegion": "CA", "addressCountry": "US"},
   "areaServed": {"@type": "City", "name": "San Francisco"}, "founder": {"@id": f"{SITE}/#owner"},
   "priceRange": "$95–$1,100", "currenciesAccepted": "USD",
   "potentialAction": {"@type": "ReserveAction", "target": BOOK, "name": "Book an appointment"},
   "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Tax services", "itemListElement": offers(PREP) + offers(ADVISORY)},
   "sameAs": []},
  {"@type": "Person", "@id": f"{SITE}/#owner", "name": OWNER, "jobTitle": "Founder", "worksFor": {"@id": f"{SITE}/#business"},
   "image": f"{SITE}/assets/img/portrait-hero-800.jpg"},
  {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "Sanchez Consulting Services", "publisher": {"@id": f"{SITE}/#business"}},
  {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"}]},
  {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(__import__("re").sub("<[^>]+>", "", a))}} for q, a in FAQ]},
]}

TITLE = "Sanchez Consulting Services | Tax Preparation & Tax Strategy in San Francisco"
DESC = "Personal, one-on-one tax preparation and tax strategy in San Francisco with Telma Sanchez Perez — individual, joint, self-employed, LLC and S-Corp returns, amendments and IRS/FTB notice help. Book online."

def head(title, desc, canonical, extra=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
{canonical}
<meta name="theme-color" content="#0b0b0c">
<meta name="author" content="Sanchez Consulting Services">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Sanchez Consulting Services">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/">
<meta property="og:image" content="{SITE}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Sanchez Consulting Services — tax preparation and tax strategy in San Francisco">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/assets/img/og-image.jpg">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/cormorant.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/jost.woff2" as="font" type="font/woff2" crossorigin>
{extra}<link rel="stylesheet" href="/css/styles.css">
<script>document.documentElement.classList.add('js')</script>
</head>'''

HEADER = f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <nav class="wrap nav" aria-label="Primary">
    <a class="brand" href="/#top" aria-label="Sanchez Consulting Services — home">
      <picture><source srcset="/assets/img/logo-horizontal-120.webp" type="image/webp"><img src="/assets/img/logo-horizontal-120.png" alt="Sanchez Consulting Services" width="405" height="120"></picture>
    </a>
    <button class="nav-toggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav-links"><span></span><span></span><span></span></button>
    <ul class="nav-links" id="nav-links">
      <li><a href="/#top">Home</a></li>
      <li><a href="/#about">About</a></li>
      <li><a href="/#services">Services</a></li>
      <li><a href="/#faq">FAQ</a></li>
      <li><a class="btn btn-gold" href="/#book">Book an Appointment</a></li>
    </ul>
  </nav>
</header>'''

FOOTER = f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <picture><source srcset="/assets/img/logo-stacked.webp" type="image/webp"><img src="/assets/img/logo-stacked.png" alt="Sanchez Consulting Services" width="420" height="313" loading="lazy"></picture>
        <p>Personal tax preparation and tax strategy in San Francisco, California.</p>
      </div>
      <div>
        <h3>Explore</h3>
        <ul><li><a href="/#about">About Telma</a></li><li><a href="/#services">Services &amp; Fees</a></li><li><a href="/#faq">Good to Know</a></li><li><a href="/#book">Book an Appointment</a></li></ul>
      </div>
      <div>
        <h3>Contact</h3>
        <ul>
          <li><a href="sms:{PHONE_TEL}">Text {PHONE_DISPLAY}</a></li>
          <!-- PLACEHOLDER: client email, e.g. <li><a href="mailto:hello@example.com">hello@example.com</a></li> -->
          <li>San Francisco, California</li>
          <li><small>Office address provided after your appointment is confirmed.</small></li>
        </ul>
      </div>
      <div>
        <h3>Scheduling</h3>
        <ul>
          <li><a href="{BOOK}" target="_blank" rel="noopener">Online scheduler</a></li>
          <li>By appointment only</li>
          <!-- PLACEHOLDER: office hours / social links (Instagram, Facebook, Google Business Profile) -->
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span id="year">2026</span> Sanchez Consulting Services LLC. All rights reserved.</span>
      <span>San Francisco, CA</span>
    </div>
  </div>
</footer>'''

def pic(name, alt, w, h, sizes, eager=False):
    ss = lambda ext: ", ".join(f"/assets/img/{name}-{x}.{ext} {x}w" for x in (420, 640, 800))
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source type="image/webp" srcset="{ss("webp")}" sizes="{sizes}">'
            f'<img src="/assets/img/{name}-640.jpg" srcset="{ss("jpg")}" sizes="{sizes}" alt="{alt}" width="{w}" height="{h}" {load}></picture>')

MARK = '<img class="mark" src="/assets/img/logo-mark.png" alt="" width="247" height="313" loading="lazy">'

faq_html = "\n".join(f'''      <details class="reveal">
        <summary>{html.escape(q)}</summary>
        <div class="answer"><p>{a}</p></div>
      </details>''' for q, a in FAQ)

INDEX = head(TITLE, DESC, f'<link rel="canonical" href="{SITE}/">',
  '<link rel="preload" as="image" type="image/webp" imagesrcset="/assets/img/portrait-hero-420.webp 420w, /assets/img/portrait-hero-640.webp 640w, /assets/img/portrait-hero-800.webp 800w" imagesizes="(max-width: 920px) 86vw, 460px">\n') + f'''
<body id="top">
{HEADER}
<main id="main">

  <!-- HERO -->
  <section class="hero dark pattern" aria-labelledby="hero-title">
    <div class="wrap hero-grid">
      <div>
        <p class="eyebrow reveal">Tax Preparation &amp; Strategy · San Francisco</p>
        <h1 id="hero-title" class="reveal d1"><span class="line">Your taxes,</span><span class="line">handled with <em class="accent gold-text">care</em></span><span class="line">&amp; precision.</span></h1>
        <p class="lede reveal d2">Sanchez Consulting Services is the San Francisco tax practice of Telma Sanchez Perez — personal, one-on-one tax preparation and tax strategy for individuals, families, the self-employed and small business owners.</p>
        <div class="hero-ctas reveal d3">
          <a class="btn btn-gold" href="#book">Book an Appointment {ARROW}</a>
          <a class="btn btn-ghost" href="#services">View Services &amp; Fees</a>
        </div>
        <div class="hero-meta reveal d3">
          <div><strong>Individuals &amp; Couples</strong>W-2 · Joint Returns</div>
          <div><strong>Business Owners</strong>Sole Prop · LLC · S-Corp</div>
          <div><strong>Advisory</strong>Strategy · Notices</div>
        </div>
      </div>
      <div class="portrait reveal d2">
        <div class="frame">
          <!-- PLACEHOLDER IMAGE until client photos are processed: run tools/build_images.py HERO.jpg ABOUT.jpg -->
          {pic("portrait-hero", "Telma Sanchez Perez, founder of Sanchez Consulting Services, San Francisco tax preparer", 800, 1200, "(max-width: 920px) 86vw, 460px", eager=True)}
        </div>
        <div class="portrait-card">
          <span>Questions before booking?</span>
          <a href="sms:{PHONE_TEL}">Text {PHONE_DISPLAY}</a>
        </div>
      </div>
    </div>
    <span class="scroll-cue" aria-hidden="true"></span>
  </section>

  <div class="ribbon" aria-label="Areas of service">
    <ul>
      <li>Individual Returns</li><li>Married Filing Jointly</li><li>Self-Employed</li><li>LLC</li><li>S-Corporation</li><li>Amendments</li><li>Tax Strategy</li>
    </ul>
  </div>

  <!-- ABOUT -->
  <section class="section" id="about" aria-labelledby="about-title">
    <div class="wrap">
      <div class="about-grid">
        <div class="about-photo reveal">
          <div class="frame">{pic("portrait-about", "Telma Sanchez Perez of Sanchez Consulting Services", 800, 1000, "(max-width: 920px) 90vw, 480px")}</div>
        </div>
        <div class="about-copy">
          <p class="eyebrow reveal">Meet Telma</p>
          <h2 id="about-title" class="reveal d1">A trusted tax professional, <em class="accent">found by referral.</em></h2>
          <p class="big reveal d2">Most clients come to Sanchez Consulting Services the same way — recommended by a family member, friend or colleague who already trusts Telma with their taxes.</p>
          <p class="reveal d2">Telma Sanchez Perez founded Sanchez Consulting Services LLC in San Francisco to give every client the kind of attention a large tax office can’t: a private appointment, a clear understanding of your situation, and a return prepared carefully from the information you provide.</p>
          <p class="reveal d3">From W-2 returns and married couples filing jointly to side businesses, LLCs and S-Corporations — plus amendments, IRS and FTB notices and year-round tax strategy — each appointment is reserved exclusively for you.</p>
          <!-- PLACEHOLDER: add Telma's credentials (e.g. PTIN / EA / AFSP), years of experience, languages spoken, and a personal line about her background once confirmed by the client. -->
          <div class="signature reveal d3">
            <img src="/assets/img/logo-mark.png" alt="" width="247" height="313" loading="lazy">
            <div><strong>Telma Sanchez Perez</strong><span>Founder · Sanchez Consulting Services</span></div>
          </div>
        </div>
      </div>
      <div class="pillars">
        <div class="pillar reveal"><span class="num">I</span><h3>One-on-one</h3><p>Every appointment is reserved exclusively for you — one return, one focused conversation.</p></div>
        <div class="pillar reveal d1"><span class="num">II</span><h3>Clear pricing</h3><p>Fees are published up front. Where complexity adds cost, it is discussed with you beforehand.</p></div>
        <div class="pillar reveal d2"><span class="num">III</span><h3>Simple booking</h3><p>Choose your appointment, complete your intake and secure your time online in minutes.</p></div>
      </div>
    </div>
  </section>

  <!-- SERVICES -->
  <section class="section services dark pattern" id="services" aria-labelledby="services-title">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow reveal">Services &amp; Fees</p>
        <h2 id="services-title" class="reveal d1">Tax preparation &amp; advisory, <em class="accent gold-text">clearly priced.</em></h2>
        <p class="reveal d2">Each tax preparation appointment covers one tax return. Choose the service that matches your situation — or text <a href="sms:{PHONE_TEL}">{PHONE_DISPLAY}</a> and Telma will schedule you.</p>
      </div>
      <div class="svc-group">
        <div class="svc-group-title reveal"><h3>Tax Preparation</h3><p>Deposit taken at booking · applied to your fee</p></div>
        <ul class="svc-list">
{svc_rows(PREP, 1)}
        </ul>
      </div>
      <div class="svc-group">
        <div class="svc-group-title reveal"><h3>Tax Advisory</h3><p>Paid in full at booking · phone, Zoom, FaceTime or in person</p></div>
        <ul class="svc-list">
{svc_rows(ADVISORY, len(PREP) + 1)}
        </ul>
      </div>
      <p class="svc-note reveal">{DEPOSIT} Business and self-employed returns require annual income and expense totals by category. Appointments after April 5 may require an extension.</p>
    </div>
  </section>

  <!-- BOOK -->
  <section class="section book" id="book" aria-labelledby="book-title">
    <div class="wrap book-grid">
      <div class="book-aside">
        <p class="eyebrow reveal">Book an Appointment</p>
        <h2 id="book-title" class="reveal d1">Reserve your time <em class="accent">with Telma.</em></h2>
        <p class="reveal d2">Scheduling and deposits are handled securely through Acuity Scheduling. Pick your service and time, complete the short intake, and your appointment is confirmed.</p>
        <ul class="policy reveal d2">
          <li>One appointment covers one tax return. Married filing jointly counts as one return.</li>
          <li>A non-refundable deposit is taken at booking and applied toward your tax preparation fee.</li>
          <li>Please give at least 24 hours’ notice to cancel or reschedule.</li>
          <li>The office address is shared after your appointment is confirmed.</li>
        </ul>
        <div class="contact-line reveal d3"><span>Not sure which to choose?</span><a href="sms:{PHONE_TEL}">Text {PHONE_DISPLAY}</a></div>
      </div>
      <div class="reveal d1">
        <div class="scheduler">
          <iframe src="{EMBED}" title="Schedule an appointment with Sanchez Consulting Services" loading="lazy" allow="payment"></iframe>
        </div>
        <p class="scheduler-fallback">Trouble viewing the scheduler? <a href="{BOOK}" target="_blank" rel="noopener">Open it in a new window</a>.</p>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="section" id="faq" aria-labelledby="faq-title" style="padding-top:0;background:var(--ivory)">
    <hr class="hairline">
    <div class="wrap" style="padding-top:clamp(5rem,9vw,7.5rem)">
      <div class="section-head center">
        <p class="eyebrow reveal">Good to Know</p>
        <h2 id="faq-title" class="reveal d1">Frequently asked questions</h2>
      </div>
      <div class="faq-list">
{faq_html}
      </div>
    </div>
  </section>

  <!-- PLACEHOLDER: TESTIMONIALS — add only real, client-approved quotes. Template:
  <section class="section" aria-labelledby="kind-words"><div class="wrap"><h2 id="kind-words">Kind words</h2>
    <blockquote><p>“Real client quote here.”</p><footer>— First name, San Francisco</footer></blockquote>
  </div></section> -->

  <section class="closing dark pattern" aria-labelledby="closing-title">
    <div class="wrap">
      {MARK}
      <h2 id="closing-title" class="reveal">Ready when <em class="accent gold-text">you are.</em></h2>
      <p class="reveal d1">Book your appointment online in a few minutes, or send a text if you have a question first.</p>
      <div class="hero-ctas reveal d2" style="justify-content:center;margin:0">
        <a class="btn btn-gold" href="#book">Book an Appointment {ARROW}</a>
        <a class="btn btn-ghost" href="sms:{PHONE_TEL}">Text {PHONE_DISPLAY}</a>
      </div>
    </div>
  </section>
</main>
{FOOTER}
<div class="mobile-book"><a class="btn btn-ghost" href="sms:{PHONE_TEL}">Text</a><a class="btn btn-gold" href="#book">Book an Appointment</a></div>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script src="/js/main.js" defer></script>
</body>
</html>
'''

NF = head("Page Not Found | Sanchez Consulting Services", "The page you were looking for could not be found. Return to Sanchez Consulting Services, tax preparation and tax strategy in San Francisco.", '<meta name="robots" content="noindex">') + f'''
<body>
{HEADER}
<main id="main" class="dark pattern notfound">
  <div class="wrap">
    <p class="code gold-text">404</p>
    <h1>This page could not be found.</h1>
    <p>The link may be outdated, or the page may have moved.</p>
    <div class="hero-ctas" style="justify-content:center">
      <a class="btn btn-gold" href="/">Return Home</a>
      <a class="btn btn-ghost" href="/#book">Book an Appointment</a>
    </div>
  </div>
</main>
{FOOTER}
<script src="/js/main.js" defer></script>
</body>
</html>
'''
import re as _re
def based(t):
    t = _re.sub(r'(href|src|srcset|imagesrcset)="/(?!/)', lambda m: f'{m.group(1)}="{BASE}', t)
    return _re.sub(r', /assets/', f', {BASE}assets/', t)
open(os.path.join(ROOT, "index.html"), "w").write(based(INDEX))
open(os.path.join(ROOT, "404.html"), "w").write(based(NF))
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url><loc>{SITE}/</loc><lastmod>2026-11-14</lastmod><changefreq>monthly</changefreq><priority>1.0</priority>
    <image:image><image:loc>{SITE}/assets/img/portrait-hero-800.jpg</image:loc></image:image></url>
</urlset>
''')
json.dump({"name": "Sanchez Consulting Services", "short_name": "Sanchez", "description": "Tax preparation & tax strategy in San Francisco",
 "start_url": BASE, "display": "standalone", "background_color": "#0b0b0c", "theme_color": "#0b0b0c",
 "icons": [{"src": BASE + "assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
           {"src": BASE + "assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"},
           {"src": BASE + "assets/img/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]},
 open(os.path.join(ROOT, "site.webmanifest"), "w"), indent=2)
print("built")
