#!/usr/bin/env python3
"""Builds the corbelmaintenance.com static site into ./site.

Edit the CONFIG and COMPANIES blocks for business details, then run:
    python3 build.py
Netlify serves the ./site folder as-is (see netlify.toml).
"""
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "site"
SRC = ROOT / "src"
IMAGES = SRC / "images"

# ---------------------------------------------------------------------------
# CONFIG — replace the bracketed placeholders with real values, then rebuild.
# Placeholders render highlighted in yellow so they're easy to spot.
# ---------------------------------------------------------------------------
CONFIG = {
    "name": "Corbel Maintenance Services",
    "domain": "https://corbelmaintenance.com",
    "phone": "[PHONE]",             # e.g. "(630) 555-0123"
    "email": "[EMAIL]",             # e.g. "hello@corbelmaintenance.com"
    "response": "[RESPONSE TIME]",  # e.g. "one business day"
    "area": "DuPage and Will County, Illinois",
}

# Each company card. "phone" is that company's own line.
COMPANIES = [
    {
        "key": "pothole", "word": "POTHOLE REPAIR", "name": "123 Pothole Repair",
        "url": "https://123pothole.com", "host": "123pothole.com",
        "tag": "Parking lot repair", "phone": "[PHONE]",
        "img": "pothole-card.jpg", "alt": "Crew heat-sealing asphalt in a parking lot",
        "desc": "Pothole patching, crack sealing, sealcoating, striping, catch basins, curbs, signs and ADA parking.",
        "covered": ("Parking lots", "Potholes, crack sealing, striping, sealcoating, catch basins, curbs, signs, ADA parking."),
    },
    {
        "key": "concrete", "word": "CONCRETE REPAIR", "name": "123 Concrete Repair",
        "url": "https://123concreterepair.com", "host": "123concreterepair.com",
        "tag": "Sidewalk and walkway repair", "phone": "[PHONE]",
        "img": "concrete-card.jpg", "alt": "Concrete sidewalk slabs along a brick commercial storefront",
        "desc": "Trip hazard shaving, concrete lifting, joint sealing, drainage fixes and paver resetting.",
        "covered": ("Sidewalks", "Trip hazard shaving, slab lifting, joint sealing, drainage, pavers."),
    },
    {
        "key": "dock", "word": "DOCK DOORS", "name": "123 Dock Doors",
        "url": "https://123dockdoors.com", "host": "123dockdoors.com",
        "tag": "Dock and overhead door service", "phone": "[PHONE]",
        "img": "dockdoors-card.jpg", "alt": "Row of loading dock doors on a warehouse",
        "desc": "Loading dock doors, rolling steel and overhead doors, openers, dock seals and bumpers.",
        "covered": ("Dock & overhead doors", "Dock doors, rolling steel and overhead doors, openers, seals and bumpers."),
    },
]

ICONS = {
    "pothole": '<path d="M3 20L8 4M21 20L16 4M12 4v2M12 9v2"/><ellipse cx="12" cy="16" rx="4" ry="2"/>',
    "concrete": '<path d="M3 6h8v5H3zM13 6h8v5h-8zM3 15h8v5H3zM13 13.5h8v5h-8z"/>',
    "dock": '<path d="M3 21V5l9-3 9 3v16M7 21V9h10v12M7 12.5h10M7 16h10"/>',
}

LOGO_MARK = ('<svg width="34" height="34" viewBox="0 0 34 34" aria-hidden="true">'
             '<path d="M2 2h30v8H24v8h-8v8H8v6H2z" fill="#2f6a94"/></svg>')

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600'
         '&family=Barlow+Condensed:wght@600;700&display=swap" rel="stylesheet">')


def is_ph(v):
    return v.startswith("[") and v.endswith("]")


def show(v):
    return f'<span class="ph">{html.escape(v)}</span>' if is_ph(v) else html.escape(v)


def val(key):
    return show(CONFIG[key])


def phone_link(v):
    if is_ph(v):
        return show(v)
    digits = "".join(c for c in v if c.isdigit())
    return f'<a href="tel:+1{digits[-10:]}">{html.escape(v)}</a>'


def email_link():
    v = CONFIG["email"]
    return show(v) if is_ph(v) else f'<a href="mailto:{v}">{html.escape(v)}</a>'


NAV = [("/#companies", "Our companies"), ("/property-managers/", "For property managers"),
       ("/#about", "About"), ("/#contact", "Contact")]


def header(path):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == path else ""}>{t}</a>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
  <a class="brand" href="/">{LOGO_MARK}<span class="brand-name">CORBEL<small>MAINTENANCE SERVICES</small></span></a>
  <nav class="nav" aria-label="Main">{links}</nav>
</div></header>'''


def footer():
    co = "".join(f'<a href="{c["url"]}">{c["name"]}</a>' for c in COMPANIES)
    return f'''<footer class="site-footer"><div class="wrap">
  <span>© 2026 {CONFIG["name"]}</span>
  <nav aria-label="Our companies">{co}<a href="/privacy/">Privacy</a></nav>
</div></footer>'''


def page(path, title, desc, body, schema=None):
    canonical = CONFIG["domain"] + path
    schema_tag = f'<script type="application/ld+json">{json.dumps(schema)}</script>' if schema else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:image" content="{CONFIG["domain"]}/images/about.jpg">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="/styles.css">
{schema_tag}
</head>
<body>
{header(path)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
'''


PAGES = {}


def add(path, title, desc, body, schema=None):
    PAGES[path] = page(path, title, desc, body, schema)


def company_card(c):
    icon = (f'<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[c["key"]]}</svg>')
    return f'''<article class="company">
  <img src="/images/{c["img"]}" alt="{html.escape(c["alt"])}" loading="lazy" width="960" height="600">
  <div class="company-bar"><span class="company-mark">{icon}</span>
    <h3 class="company-name"><b>123</b> {c["word"]}<small>{c["tag"]}</small></h3></div>
  <div class="company-body">
    <p>{c["desc"]}</p>
    <p class="phone">Call {phone_link(c["phone"])}</p>
    <a class="btn btn-orange" href="{c["url"]}">Visit {c["host"]}</a>
  </div>
  <p class="company-foot">A CORBEL COMPANY</p>
</article>'''


def honeypot(form):
    return (f'<input type="hidden" name="form-name" value="{form}">'
            '<p class="hidden"><label>Leave this empty <input name="website_url"></label></p>')


# Home ------------------------------------------------------------------------
schema_home = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": CONFIG["name"],
    "url": CONFIG["domain"],
    "description": "Locally owned family of property maintenance companies serving DuPage and Will County, Illinois.",
    "areaServed": [{"@type": "AdministrativeArea", "name": "DuPage County, IL"},
                   {"@type": "AdministrativeArea", "name": "Will County, IL"}],
    "subOrganization": [{"@type": "HomeAndConstructionBusiness", "name": c["name"], "url": c["url"]} for c in COMPANIES],
}

POINTS = [
    ("Clear responsibility", "Every job is quoted, contracted and invoiced by the company that does the work."),
    ("Specialists, not generalists", "Each company does one kind of work and does it well."),
    ("Same standards everywhere", "Written quotes, before and after photos, and clean, coned work zones on every job."),
    ("Locally owned", "Owner-run and based in DuPage and Will County."),
]

add("/", "Corbel Maintenance Services | Parking Lot, Sidewalk & Dock Door Specialists",
    "Corbel Maintenance Services is the family of local companies that keep commercial properties in DuPage and Will County safe: parking lots, sidewalks, and dock and overhead doors.",
    f'''<section class="hero"><div class="wrap">
  <p class="kicker">DuPage and Will County, Illinois</p>
  <h1>Everything outside your building, handled by specialists.</h1>
  <p class="lead">Corbel Maintenance Services is the family of local companies that keep commercial properties safe and working: parking lots, sidewalks, and dock and overhead doors.</p>
  <div class="btns"><a class="btn btn-primary" href="#companies">See our companies</a>
    <a class="btn btn-ghost" href="/property-managers/">Managing several properties?</a></div>
</div></section>

<section class="section" id="companies"><div class="wrap">
  <h2>Our companies</h2>
  <p class="intro">Three independent companies, each with its own crews, its own phone line and its own website. Contact the one you need directly.</p>
  <div class="companies">{"".join(company_card(c) for c in COMPANIES)}</div>
</div></section>

<section class="section section-white"><div class="wrap">
  <h2 class="solo">Why work with a Corbel company</h2>
  <div class="points">{"".join(f'<div><p class="num">0{i}</p><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(POINTS, 1))}</div>
</div></section>

<section class="section" id="about"><div class="wrap about">
  <div>
    <h2>About Corbel</h2>
    <p>A corbel is the bracket that holds up what sits above it. That's the job: the parking lots, walks and doors that a building depends on but nobody thinks about until they fail.</p>
    <p>Corbel is locally owned and operated, with every company run to the same standards.</p>
  </div>
  <img src="/images/about.jpg" alt="Commercial building with overhead doors, a paved lot and a front walkway" loading="lazy" width="1000" height="750">
</div></section>

<section class="section contact" id="contact"><div class="wrap split">
  <div>
    <h2>Tell us what needs fixing</h2>
    <p class="sub">We'll pass it to the right company, which will quote you directly within {val("response")}.</p>
    <p class="sub">Phone {phone_link(CONFIG["phone"])}<br>Email {email_link()}</p>
  </div>
  <form class="form" name="contact" method="POST" action="/thank-you/" data-netlify="true" netlify-honeypot="website_url">
    {honeypot("contact")}
    <div><label for="c-name">Name</label><input id="c-name" name="name" autocomplete="name" required></div>
    <div><label for="c-email">Email</label><input id="c-email" type="email" name="email" autocomplete="email" required></div>
    <div><label for="c-phone">Phone</label><input id="c-phone" type="tel" name="phone" autocomplete="tel"></div>
    <div><label for="c-co">Company or property</label><input id="c-co" name="company" autocomplete="organization"></div>
    <div class="full"><label for="c-addr">Property address</label><input id="c-addr" name="address" autocomplete="street-address" required></div>
    <div class="full"><label for="c-svc">What do you need?</label>
      <select id="c-svc" name="service">
        <option>Parking lot (potholes, sealing, striping)</option>
        <option>Sidewalks (trip hazards, sunken slabs)</option>
        <option>Dock or overhead doors</option>
        <option>Several of these</option>
        <option>Not sure</option>
      </select></div>
    <div class="full"><label for="c-notes">Details</label><textarea id="c-notes" name="notes" rows="3"></textarea></div>
    <div class="full"><button class="btn btn-primary" type="submit">Send request</button></div>
  </form>
</div></section>''', schema_home)

# For property managers ---------------------------------------------------------
SHARED = [
    ("Written quotes", "Clear scope and price before any work starts."),
    ("Photo reports", "Before and after photos in the same format, whichever company did the job."),
    ("Coordinated site visits", "One walk-through can cover lot, sidewalk and door needs at the same property."),
]
STEPS = [
    ("Send your property list", "Addresses and any known problem spots."),
    ("We walk every site", "Lots, walks and doors, photographed and measured."),
    ("Each company quotes its work", "Safety fixes first, priced by property."),
    ("Photo reports after every job", "Before and after photos, ready to send to owners."),
]

add("/property-managers/", "For Property Managers | Corbel Maintenance Services",
    "One walk-through for the parking lots, sidewalks and dock doors across your DuPage and Will County portfolio, with specialist companies quoting each trade.",
    f'''<section class="hero hero-sub"><div class="wrap">
  <p class="kicker">For property managers and portfolios</p>
  <h1>Specialists for every lot, walk and door you manage.</h1>
  <p class="lead">Corbel's companies each focus on one trade and work to the same standards across your portfolio.</p>
  <a class="btn btn-primary" href="#start">Schedule a portfolio walk-through</a>
</div></section>

<section class="section"><div class="wrap">
  <h2>What every Corbel company shares</h2>
  <p class="intro">Each company quotes, contracts and invoices its own work, so you always know who is responsible. What they share is how they work.</p>
  <div class="tiles">{"".join(f'<div class="tile"><h3>{t}</h3><p>{d}</p></div>' for t, d in SHARED)}</div>
</div></section>

<section class="section section-white"><div class="wrap">
  <h2 class="solo">How a portfolio program works</h2>
  <ol class="steps">{"".join(f'<li><span class="n">{i}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(STEPS, 1))}</ol>
</div></section>

<section class="section"><div class="wrap">
  <h2 class="solo">What's covered</h2>
  <div class="covered">{"".join(f'<div><h3><a href="{c["url"]}">{c["covered"][0]} · {c["name"]}</a></h3><p>{c["covered"][1]}</p></div>' for c in COMPANIES)}</div>
</div></section>

<section class="section contact contact-accent" id="start"><div class="wrap split">
  <div>
    <h2>Start with a free walk-through</h2>
    <p class="sub">Tell us how many properties you manage and we'll set up a time. Prefer to talk? Call {phone_link(CONFIG["phone"])}.</p>
  </div>
  <form class="form form-card" name="walkthrough" method="POST" action="/thank-you/" data-netlify="true" netlify-honeypot="website_url">
    {honeypot("walkthrough")}
    <div><label for="p-name">Name</label><input id="p-name" name="name" autocomplete="name" required></div>
    <div><label for="p-co">Management company</label><input id="p-co" name="company" autocomplete="organization" required></div>
    <div><label for="p-email">Email</label><input id="p-email" type="email" name="email" autocomplete="email" required></div>
    <div><label for="p-phone">Phone</label><input id="p-phone" type="tel" name="phone" autocomplete="tel"></div>
    <div class="full"><label for="p-count">Properties in DuPage or Will</label>
      <select id="p-count" name="properties"><option>1–5</option><option>6–20</option><option>21–50</option><option>More than 50</option></select></div>
    <div class="full"><button class="btn btn-dark" type="submit">Request a walk-through</button></div>
  </form>
</div></section>''')

# Thank you / privacy / 404 --------------------------------------------------------
add("/thank-you/", "Thanks | Corbel Maintenance Services", "Your request was received.",
    f'''<section class="hero hero-sub"><div class="wrap">
  <h1>Thanks, we've got your request</h1>
  <p class="lead">The right Corbel company will reply within {val("response")}. Need it sooner? Call {phone_link(CONFIG["phone"])}.</p>
  <a class="btn btn-ghost" href="/">Back to home</a>
</div></section>''')

add("/privacy/", "Privacy | Corbel Maintenance Services", "How Corbel Maintenance Services handles information you send us.",
    f'''<section class="hero hero-sub"><div class="wrap"><h1>Privacy</h1>
  <p class="lead">What we do with the information you send us.</p></div></section>
<section class="section"><div class="wrap content">
  <p>When you submit a form on this site, we collect the details you enter, such as your name, contact information and property address. We use them only to respond to your request, which may include passing them to the Corbel company that will quote the work.</p>
  <p>We don't sell your information. We may store it in our customer management and email tools so our team can respond to you.</p>
  <p>To ask about or delete the information we hold, contact us at {email_link()}.</p>
  <p>Last updated: October 2026.</p>
</div></section>''')

NOT_FOUND = page("/404.html", "Page not found | Corbel Maintenance Services", "Page not found.",
                 '''<section class="hero hero-sub"><div class="wrap"><h1>That page isn't here</h1>
  <p class="lead">Try the home page to find the company you need.</p><a class="btn btn-ghost" href="/">Home</a></div></section>'''
                 ).replace(f'<link rel="canonical" href="{CONFIG["domain"]}/404.html">', "")

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 34 34"><rect width="34" height="34" rx="5" fill="#1f2125"/>'
           '<path d="M5 5h24v6.5h-6.5V18H16v6.5H9.5V29H5z" fill="#2f6a94"/></svg>')


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for path, doc in PAGES.items():
        target = OUT / "index.html" if path == "/" else OUT / path.strip("/") / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(doc, encoding="utf-8")
    (OUT / "404.html").write_text(NOT_FOUND, encoding="utf-8")
    shutil.copy(SRC / "styles.css", OUT / "styles.css")
    shutil.copytree(IMAGES, OUT / "images")
    (OUT / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    urls = "".join(f"<url><loc>{CONFIG['domain']}{p}</loc></url>" for p in PAGES if p != "/thank-you/")
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>',
        encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {CONFIG['domain']}/sitemap.xml\n", encoding="utf-8")
    print(f"Built {len(PAGES)} pages into {OUT}")


if __name__ == "__main__":
    build()
