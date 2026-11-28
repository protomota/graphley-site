#!/usr/bin/env python3
"""Writes the graphley-site pages (index, download, mcp, help, privacy, 404) on the house app-site
template, with one shared head, header and footer. tools/family.html is the template's home-page
tail (community and newsletter callouts, </main>, the More from Project ATOM block), kept unchanged
apart from the app name.

The current release (version, build, size, SHA-256) is read back from the download page, so
regenerating keeps whatever tools/set-release.sh last wrote. Not deployed (see .vercelignore).
Run from anywhere: python3 tools/build-site.py"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://graphley.ai"
GA = "G-5X9MHZPLGK"
DESC = ("Graphley is a free, local-first analytics app for Mac. It puts every website and App Store app you run "
        "in one dashboard, from Google Analytics and App Store Connect, with no Graphley server. Your AI agents "
        "can set it up through its built-in MCP server. Free and source available. iPhone and iPad beta on TestFlight.")
TITLE = "Graphley · Your sites and apps in one dashboard, on your Mac"
FAMILY = open(os.path.join(ROOT, "tools", "family.html")).read()


def current_release():
    """Version, build, size text and SHA-256 that set-release.sh last wrote to the download page."""
    rel = {"version": "0.1.0", "build": "2", "size": "Size pending", "sha": "pending"}
    try:
        page = open(os.path.join(ROOT, "download", "index.html")).read()
    except FileNotFoundError:
        return rel
    for key in rel:
        m = re.search(rf'data-release="{key}">([^<]*)<', page)
        if m:
            rel[key] = m.group(1)
    return rel


REL = current_release()
DMG = f"/downloads/Graphley-{REL['version']}.dmg"


def rel(key):
    tag = "code" if key == "sha" else "span"
    return f'<{tag} data-release="{key}">{REL[key]}</{tag}>'


ORG = {"@type": "Organization", "@id": "https://projectatom.ai/#org", "name": "Project ATOM", "url": "https://projectatom.ai/",
       "logo": "https://projectatom.ai/action/atom/atom-lockup.webp"}
APP = {"@type": "SoftwareApplication", "@id": f"{SITE}/#app", "name": "Graphley", "url": f"{SITE}/", "description": DESC,
       "applicationCategory": "BusinessApplication", "applicationSubCategory": "Web and app analytics",
       "operatingSystem": "macOS 14 or later", "softwareVersion": REL["version"], "isAccessibleForFree": True,
       "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "availability": "https://schema.org/InStock"},
       "downloadUrl": SITE + DMG, "installUrl": f"{SITE}/download/",
       "image": f"{SITE}/assets/icon.png?v=20261124",
       "featureList": ["Every website and App Store app in one dashboard", "Google Analytics 4, App Store Connect, Search Console, Bing and follower sources",
                       "Dashboards you build from charts and numbers", "Compare any period with the one before",
                       "Keys kept in the Keychain, never on a server", "Signed automatic updates",
                       "Built-in MCP server with 23 tools for Claude Code, Codex and Claude chat"],
       "author": {"@id": "https://projectatom.ai/#org"}, "publisher": {"@id": "https://projectatom.ai/#org"},
       "sameAs": ["https://projectatom.ai/apps"]}

APPLE = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/></svg>'
TESTFLIGHT = "https://testflight.apple.com/join/fVEtgQ7n"
TF_NOTE = "iPhone and iPad companion beta. Pairs with the Mac&nbsp;app."
TF_BUTTON = f'<a class="button secondary testflight-button" href="{TESTFLIGHT}" target="_blank" rel="noopener noreferrer">{APPLE} Join the TestFlight beta <span aria-hidden="true">↗</span></a>'
ICON_ARROW = '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
ICON_CHART = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 5-6"/></svg>'
ICON_PLUG = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22v-5"/><path d="M15 8V2"/><path d="M17 8a1 1 0 0 1 1 1v4a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V9a1 1 0 0 1 1-1z"/><path d="M9 8V2"/></svg>'
ICON_BOOK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/></svg>'
ICON_ACTION = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19.414 14.414C21 12.828 22 11.5 22 9.5a5.5 5.5 0 0 0-9.591-3.676.6.6 0 0 1-.818.001A5.5 5.5 0 0 0 2 9.5c0 2.3 1.5 4 3 5.5l5.535 5.362a2 2 0 0 0 2.879.052 2.12 2.12 0 0 0-.004-3 2.124 2.124 0 1 0 3-3 2.124 2.124 0 0 0 3.004 0 2 2 0 0 0 0-2.828l-1.881-1.882a2.41 2.41 0 0 0-3.409 0l-1.71 1.71a2 2 0 0 1-2.828 0 2 2 0 0 1 0-2.828l2.823-2.762"/></svg>'
ICON_CHAT = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 17a2 2 0 0 1-2 2H6.828a2 2 0 0 0-1.414.586l-2.202 2.202A.71.71 0 0 1 2 21.286V5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2z"/></svg>'
ICON_HOME = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>'
ICON_HELP = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/></svg>'

NAV = [("/#dashboards", "Dashboards", "nav-hide"), ("/#iphone", "iPhone", "nav-hide"), ("/#agents", "Agents", "nav-hide"), ("/mcp/", "MCP setup", "nav-hide-sm")]
FOOT_NAV = [("/download/", "Download"), ("/mcp/", "MCP setup"), ("/help/", "Support"), ("/privacy/", "Privacy"), ("/terms/", "Terms"),
            ("https://projectatom.ai/", "Project ATOM"), ("https://projectatom.ai/apps?app=graphley#feedback", "Send Feedback")]


def ld(graph):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")) + "</script>"


def head(path, title, desc, graph, noindex=False, home=False):
    url = SITE + path
    meta = []
    if noindex:
        meta.append('  <meta name="robots" content="noindex">')
    else:
        meta.append(f'  <meta name="description" content="{desc}">')
    meta += ['  <meta name="theme-color" content="#e6edeb" media="(prefers-color-scheme: light)">',
             '  <meta name="theme-color" content="#0b1b21" media="(prefers-color-scheme: dark)">']
    if not noindex:
        meta += [
            f'  <link rel="canonical" href="{url}">',
            '  <meta property="og:type" content="website">', '  <meta property="og:site_name" content="Graphley">',
            '  <meta property="og:locale" content="en_US">',
            f'  <meta property="og:title" content="{title}">', f'  <meta property="og:description" content="{desc}">',
            f'  <meta property="og:url" content="{url}">', f'  <meta property="og:image" content="{SITE}/social-card.png?v=20261124">',
            '  <meta property="og:image:type" content="image/png">',
            '  <meta property="og:image:width" content="1200">', '  <meta property="og:image:height" content="630">',
            '  <meta property="og:image:alt" content="Graphley. Every site and app, one calm chart. Analytics for your Mac. Free and source available.">',
            '  <meta name="twitter:card" content="summary_large_image">',
            f'  <meta name="twitter:title" content="{title}">', f'  <meta name="twitter:description" content="{desc}">',
            f'  <meta name="twitter:image" content="{SITE}/social-card.png?v=20261124">',
            '  <meta name="author" content="Project ATOM">']
    if home:
        meta += ['  <meta name="google-site-verification" content="0vROIKaO6XMvtjj9IjCOEPsr26qcvrqohH7mbLpWpfk">',
                 '  <meta name="msvalidate.01" content="E2001B47E91F72A19BB1E8E642B26928">']
    meta += ['  <link rel="icon" href="/favicon.png?v=20261124" type="image/png">', '  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png?v=20261124">',
             '  <link rel="preload" href="/assets/fonts/bricolage-grotesque-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>',
             '  <link rel="stylesheet" href="/assets/site.css">',
             '  <link rel="stylesheet" href="/atom-family.css">' if home else None,
             '  <link rel="stylesheet" href="/project-atom/project-atom-promo.css?v=20261126b">' if home else None,
             f'  <script src="/assets/analytics.js" data-ga="{GA}" data-site="graphley" data-host="graphley.ai" data-privacy="/privacy/" data-footer=".footer nav" data-css="/assets/analytics.css" defer></script>',
             '  <script src="/assets/site.js" defer></script>' if home else None,
             '  <script src="/assets/share.js" defer></script>' if home else None,
             f'  <title>{title}</title>', ('  ' + ld(graph)) if graph else None]
    return '<!doctype html>\n<html lang="en">\n<head>\n  <meta charset="utf-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n' + "\n".join(m for m in meta if m) + "\n</head>\n"


def header(current=None, body_class=None):
    links = "\n".join(f'        <a class="{c}" href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for h, t, c in NAV)
    if current == "/download/":
        cta = f'<a class="nav-cta" href="#install">{ICON_BOOK}Install guide</a>'
        links = ""
    else:
        cta = f'<a class="nav-cta" href="/download/">{APPLE} Download for Mac</a>'
    body = f'<body class="{body_class}">' if body_class else "<body>"
    return f'''{body}
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="shell nav">
      <a class="wordmark" href="/" aria-label="Graphley home"><img src="/assets/icon.png?v=20261124" alt="" width="30" height="30">Graphley</a>
      <nav aria-label="Main">
{links + chr(10) if links else ""}        {cta}
      </nav>
    </div>
  </header>
'''


def footer(family=False, status=True):
    nav = "".join(f'<a href="{h}">{t}</a>' for h, t in FOOT_NAV)
    bar = '\n    <div class="statusbar" aria-hidden="true"><div class="shell"><span><i></i>Synced to iCloud</span><span class="grow"></span><span>Last 30 days</span><span>All sites</span><span>Refreshed 7:02 AM</span></div></div>' if status else ""
    return (FAMILY if family else "") + f'''  <footer>
    <div class="shell footer">
      <a class="product-credit" href="https://projectatom.ai/" target="_blank" rel="noopener noreferrer"><img src="/project-atom/atom-icon.svg?v=20261127" width="24" height="24" alt="" style="width:24px;height:24px;border-radius:7px;box-shadow:0 0 0 1px rgba(255,255,255,.12);outline:0;border:0;filter:none"><span>A Project ATOM project</span></a>
      <nav aria-label="Footer">{nav}</nav>
    </div>
    <div class="shell footer-credit">
      <span>Hosted on Cloudflare</span>
    </div>{bar}
  </footer>
  <script src="/assets/pm-year.js" defer></script>
</body>
</html>
'''


def crumbs(name, path):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Graphley", "item": SITE + "/"},
                                                           {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]}


def webpage(path, name, desc):
    return {"@type": "WebPage", "@id": f"{SITE}{path}#webpage", "url": SITE + path, "name": name, "description": desc,
            "isPartOf": {"@id": f"{SITE}/#website"}, "inLanguage": "en-US", "publisher": {"@id": "https://projectatom.ai/#org"},
            "about": {"@id": f"{SITE}/#app"}}


def write(rel_path, html):
    p = os.path.join(ROOT, rel_path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(html)


# Made-up sample sites for the preview. Never real numbers.
SITES = [("harbor", "Harbor Notes", "k1"), ("field", "Field Guide", "k2"), ("tidepool", "Tidepool", "k3"),
         ("lantern", "Lantern Docs", "k4"), ("drift", "Driftwood", "k5")]


def window():
    side = "\n".join(f'                <button type="button" class="site" data-site-to="{i}" aria-pressed="false"><span class="dot {k}"></span>{n}<span class="n">–</span></button>' for i, n, k in SITES)
    legend = "".join(f'<span data-site="{i}"><i class="{k}"></i>{n}</span>' for i, n, k in SITES)
    return f'''        <div class="stage">
          <div class="gw" data-appearance="light" role="group" aria-label="Working preview of the Graphley window, with sample data">
            <div class="gw-title">
              <span class="lights" aria-hidden="true"><i></i><i></i><i></i></span>
              <b>Graphley</b>
              <span class="grow"></span>
              <span class="seg" role="group" aria-label="Date range">
                <button type="button" data-days="7" aria-pressed="false">7D</button>
                <button type="button" data-days="30" aria-pressed="true">30D</button>
                <button type="button" data-days="90" aria-pressed="false">90D</button>
              </span>
              <span class="sync"><i></i><span>Synced to iCloud</span></span>
            </div>
            <div class="gw-body">
              <div class="gw-side">
                <span class="side-label">Overview</span>
                <button type="button" class="site" data-site-to="all" aria-pressed="true"><span class="dot k1"></span>All sites<span class="n">5</span></button>
                <span class="side-label">Sites and apps</span>
{side}
              </div>
              <div class="gw-main">
                <div class="gw-head"><h3 data-k="title">All sites</h3><p data-k="sub">5 sites and apps · last 30 days</p></div>
                <div class="gw-kpis">
                  <div class="gw-kpi" data-i="0"><div class="l">Visitors</div><div class="v">–</div><div class="d"></div></div>
                  <div class="gw-kpi" data-i="1"><div class="l">App downloads</div><div class="v">–</div><div class="d"></div></div>
                  <div class="gw-kpi" data-i="2"><div class="l">Key events</div><div class="v">–</div><div class="d"></div></div>
                  <div class="gw-kpi"><div class="l">App Store rating</div><div class="v">4.8</div><div class="d">★ 212 ratings</div></div>
                </div>
                <div class="gw-chart">
                  <div class="gw-chart-head"><b>Visitors per day</b><span class="gw-legend">{legend}</span><span class="gw-readout" aria-live="polite"></span></div>
                  <svg viewBox="0 0 640 200" role="img" aria-label="Line chart of visitors per day, one line per site"></svg>
                </div>
                <div class="gw-foot"><span>Sources: <b>Google Analytics 4</b> · <b>App Store Connect</b></span><span>Refreshed 7:02 AM</span></div>
              </div>
            </div>
          </div>
          <div class="stage-note">
            <span>A working preview with sample data. Pick a site, change the range, or hover the chart.</span>
            <span class="chooser"><span id="look-label">Appearance</span>
              <span class="opts" role="group" aria-labelledby="look-label">
                <button type="button" data-look="light" aria-pressed="true">Light</button>
                <button type="button" data-look="dark" aria-pressed="false">Dark</button>
              </span>
            </span>
          </div>
        </div>
'''


def spark(k, pts):
    d = " ".join(("M" if i == 0 else "L") + f"{i * 56 / (len(pts) - 1):.1f} {19 - p:.1f}" for i, p in enumerate(pts))
    return f'<svg viewBox="0 0 56 20" aria-hidden="true"><path class="{k}" d="{d}"/></svg>'


def phone():
    rows = [("k1", "Harbor Notes", "App site", "612", "▲ 18%", "", [4, 6, 5, 8, 9, 12, 14]),
            ("k3", "Tidepool", "iPhone app", "148", "▲ 31%", "", [3, 4, 6, 5, 9, 11, 16]),
            ("k2", "Field Guide", "Blog", "377", "▲ 6%", "", [8, 7, 9, 8, 10, 9, 11]),
            ("k4", "Lantern Docs", "Docs", "121", "▼ 4%", "down", [10, 11, 9, 9, 8, 9, 8])]
    out = "\n".join(f'              <div class="phone-row"><i class="{k}"></i><span><b>{n}</b><small>{s}</small></span><span class="num">{v}{spark(k, p)}<em class="{c}">{d}</em></span></div>' for k, n, s, v, d, c, p in rows)
    return f'''        <figure class="phone">
          <div class="phone-frame">
            <div class="phone-screen">
              <h4>Today</h4>
              <p class="sub">Visitors so far · synced 7:02 AM</p>
{out}
            </div>
          </div>
          <figcaption>iPhone and iPad beta on TestFlight · sample data</figcaption>
        </figure>
'''


INSTALL_STEPS = [("Open the disk image", "and drag Graphley into Applications."),
                 ("Launch Graphley", "and sign in with Google to find your Google Analytics properties."),
                 ("Pick what to track,", "add an App Store Connect key if you have apps, and your dashboard fills in.")]


def index():
    graph = [{"@type": "WebSite", "@id": f"{SITE}/#website", "url": SITE + "/", "name": "Graphley", "description": DESC, "inLanguage": "en-US",
              "publisher": {"@id": "https://projectatom.ai/#org"}},
             {**webpage("/", TITLE, DESC), "mainEntity": {"@id": f"{SITE}/#app"}}, APP, ORG]
    steps = "\n".join(f'          <li><span><strong>{a}</strong> {b}</span></li>' for a, b in INSTALL_STEPS)
    h = head("/", TITLE, DESC, graph, home=True) + header()
    h += f'''
  <main id="main">
    <section class="hero" aria-labelledby="hero-title">
      <div class="shell">
        <p class="pill"><i></i>Mac app · Free · Source available</p>
        <h1 id="hero-title">Every site and app. <em>One calm chart.</em></h1>
        <p class="lead">Graphley puts your websites and App Store apps in one dashboard on your Mac. It reads Google Analytics and App Store Connect directly, keeps your keys in the Keychain, and runs no server of its own. <strong>Your AI agents can set it up for you.</strong></p>
        <div class="actions">
          <a class="button" href="/download/">{APPLE} Download for Mac</a>
          <a class="button secondary" href="#dashboards">{ICON_CHART}See what it does</a>
          <button type="button" class="pm-share-btn gx-share" data-pm-share data-share-url="{SITE}/" data-share-title="Graphley" data-share-text="Every site and app in one calm chart, on your Mac. Free." aria-haspopup="menu" aria-label="Share Graphley"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12"/><path d="m7.5 7.5 4.5-4.5 4.5 4.5"/><path d="M5 12v6.5A2.5 2.5 0 0 0 7.5 21h9a2.5 2.5 0 0 0 2.5-2.5V12"/></svg><span data-pm-share-label>Share</span></button>
        </div>
        <p class="fineprint">Free · Source available · macOS 14 or later · Version {rel("version")}</p>

{window()}
        <dl class="facts">
          <div><dt>0</dt><dd>Graphley servers. Your numbers stay on your devices</dd></div>
          <div><dt>2</dt><dd>sources: Google Analytics 4 and App Store Connect</dd></div>
          <div><dt>16</dt><dd>MCP tools for the agent you connect</dd></div>
          <div><dt>$0</dt><dd>free and source available</dd></div>
        </dl>
      </div>
    </section>

    <section id="dashboards" class="section">
      <div class="shell">
        <div class="section-head">
          <span class="mark">dashboards</span>
          <h2>All of it, <em>in one place.</em></h2>
          <p class="lead">If you run more than one site or app, the numbers live in five different consoles. Graphley pulls them into one window, one color per site, so you can see the whole picture before your coffee is cold.</p>
        </div>
        <div class="bento">
          <article class="card wide">
            <h3>Google Analytics, without the console</h3>
            <p>Sign in with Google once. Graphley finds every GA4 property you can read and asks which ones to track. Visitors, page views, key events and top pages come straight from Google’s Data API.</p>
            <div class="visual"><div class="mini" aria-hidden="true">
              <div class="mini-row"><span class="lbl">Found</span><span class="val">7 GA4 properties</span><span class="end">2 accounts</span></div>
              <div class="mini-row"><span class="lbl">Tracking</span><span class="val"><b>harbornotes.app</b>, <b>fieldguide.blog</b> …</span><span class="end">5</span></div>
            </div></div>
          </article>
          <article class="card wide">
            <h3>App Store downloads and ratings</h3>
            <p>Add an App Store Connect key and Graphley reads your daily sales reports: first-time downloads by app and by device, next to each app’s rating and review count.</p>
            <div class="visual"><div class="mini" aria-hidden="true">
              <div class="mini-row"><span class="lbl">Tidepool</span><span class="val">iPhone <b>112</b> · iPad <b>36</b></span><span class="end">★ 4.8</span></div>
              <div class="mini-row"><span class="lbl">Harbor</span><span class="val">Mac <b>64</b></span><span class="end">★ 4.6</span></div>
            </div></div>
          </article>
          <article class="card">
            <h3>Dashboards you build</h3>
            <p>Make a dashboard for a launch, a client or a morning check. Add line charts, bars and single numbers from any source.</p>
          </article>
          <article class="card">
            <h3>Compare periods</h3>
            <p>Every number shows how it moved against the period before, so a quiet week stands out at a glance.</p>
            <div class="visual"><ul class="chips"><li>7 days</li><li>30 days</li><li>90 days</li></ul></div>
          </article>
          <article class="card">
            <h3>Refresh on your schedule</h3>
            <p>Graphley refreshes in the morning and whenever you ask. A source that fails is skipped and flagged, and the rest still update.</p>
          </article>
        </div>
      </div>
    </section>

    <section id="iphone" class="section band">
      <div class="shell split">
        <div>
          <span class="mark">iphone and ipad · testflight beta</span>
          <h2>Check it <em>from anywhere.</em></h2>
          <p class="lead">The iPhone and iPad app is in beta on TestFlight. It shows the same numbers as your Mac: your Mac does the fetching and writes a snapshot to your private iCloud database, and your iPhone reads&nbsp;it.</p>
          <ul class="ticks">
            <li><span><strong>Your iCloud, not ours.</strong> Data syncs through your own private CloudKit database. Graphley has no server to send it to.</span></li>
            <li><span><strong>Keys stay on the Mac.</strong> Google and App Store Connect credentials live in the Keychain and never travel with the numbers.</span></li>
            <li><span><strong>Fresh in the morning.</strong> When the Mac refreshes, the phone gets a quiet push and updates.</span></li>
          </ul>
          <div class="actions actions-left">
            {TF_BUTTON}
          </div>
          <p class="fineprint">{TF_NOTE}</p>
        </div>
{phone()}      </div>
    </section>

    <section id="agents" class="section">
      <div class="shell agent">
        <div>
          <span class="mark">agents</span>
          <h2>Let your agent <em>do the setup.</em></h2>
          <p class="lead">Graphley has an MCP server built in. Connect Claude Code, Codex or Claude chat and it can find your Google Analytics properties, add sites and apps, build dashboards and answer questions about your numbers. Every change it makes is logged in the app.</p>
          <div class="clients">
            <a href="/mcp/#claude-code">{ICON_PLUG}Claude Code <span aria-hidden="true">→</span></a>
            <a href="/mcp/#codex">{ICON_PLUG}Codex <span aria-hidden="true">→</span></a>
            <a href="/mcp/#claude-chat">{ICON_PLUG}Claude chat <span aria-hidden="true">→</span></a>
          </div>
          <div class="actions"><a class="button secondary" href="/mcp/">{ICON_BOOK}How agent setup works</a></div>
        </div>
        <div class="session" data-mode="write">
          <div class="session-bar">
            <span id="mode-label">Graphley › Settings › Agents</span>
            <span class="chooser"><span class="opts" role="group" aria-labelledby="mode-label">
              <button type="button" data-mode-to="read" aria-pressed="false">View only</button>
              <button type="button" data-mode-to="write" aria-pressed="true">Can make changes</button>
            </span></span>
          </div>
          <div class="session-body">
            <p class="say you">I just launched tidepool.app. Track it, and add it to my Launch dashboard.</p>
            <ul class="calls">
              <li><div><b>discover_ga4_properties</b><span>7 properties · “Tidepool” not tracked yet</span></div></li>
              <li class="only-write"><div><b>add_site</b><span>Tidepool · GA4 property 482913077</span></div></li>
              <li class="only-write"><div><b>add_widget</b><span>Launch › Visitors per day · Tidepool</span></div></li>
              <li class="only-write"><div><b>refresh_all</b><span>5 sites · 2 apps refreshed</span></div></li>
              <li class="only-read blocked"><div><b>add_site</b><span>Agents can view only. Turn on “Let agents make changes” in Settings → Agents.</span></div></li>
            </ul>
            <p class="say agent-says only-write">Done. Tidepool is tracked and on your Launch dashboard. It had 148 visitors yesterday.</p>
            <p class="say agent-says only-read">I found the Tidepool property. Graphley is set to view only, so I haven’t added it.</p>
          </div>
        </div>
      </div>
    </section>

    <section id="privacy" class="section band" aria-labelledby="privacy-title">
      <div class="shell">
        <div class="section-head">
          <span class="mark">privacy</span>
          <h2 id="privacy-title">Your numbers stay <em>yours.</em></h2>
        </div>
        <div class="trio">
          <div><h3>No Graphley server</h3><p>Graphley talks to Google and Apple directly from your Mac. There’s no account to make and nothing for us to store.</p></div>
          <div><h3>Keys in the Keychain</h3><p>Sign-in tokens and App Store Connect keys are kept in the Keychain. They never go into synced data or into an agent’s hands.</p></div>
          <div><h3>Agents on your terms</h3><p>The MCP server runs on your Mac. You choose whether agents can only look, or can also make changes. <a href="/privacy/#mcp">How agent access works</a></p></div>
        </div>
      </div>
    </section>

    <section id="download" class="section" aria-labelledby="download-title">
      <div class="shell split install">
        <div>
          <span class="mark">download</span>
          <h2 id="download-title">Graphley for <em>Mac.</em></h2>
          <p class="lead">Free for Macs running macOS 14 or later. Code signed, notarized by Apple, and kept up to date automatically.</p>
          <div class="actions">
            <a class="button" href="/download/">{APPLE} Download and install</a>
            <a class="button secondary" href="/mcp/">{ICON_PLUG}MCP setup</a>
            {TF_BUTTON}
          </div>
          <p class="fineprint">{TF_NOTE}</p>
        </div>
        <ol class="install-steps" aria-label="Getting started">
{steps}
        </ol>
      </div>
    </section>

'''
    # Community and newsletter callouts, </main> and the More from Project ATOM block come from the template.
    h += footer(family=True)
    write("index.html", h)


WHATS_NEW = [("Dashboards", "An overview of every site and app, a page per site, and dashboards you build from line charts, bars and numbers."),
             ("Google Analytics 4", "Sign in with Google once (read-only). Visitors, new visitors, sessions, page views, key events and top pages."),
             ("App Store Connect", "First downloads and redownloads by app and device from your daily sales reports, plus ratings and written reviews from every storefront."),
             ("Search and followers", "Google Search Console and Bing Webmaster Tools clicks, impressions and position per site, and follower counts from X, Instagram, YouTube and GitHub."),
             ("Compare periods", "7, 30 and 90 days, each against the period before."),
             ("Morning refresh", "Refreshes at the hour you choose, on launch if it missed one, or with ⌘R. A failing source never blocks the others."),
             ("MCP server", "23 tools for Claude Code, Codex and Claude chat, with view-only and key-saving switches, and a log of every agent change."),
             ("Automatic updates", "Signed updates through Sparkle. Graphley checks for new versions and installs them for you.")]


def download():
    d = "Download Graphley for Mac. Free, signed and notarized, with automatic updates. Install it, sign in with Google and pick the sites to track."
    graph = [webpage("/download/", "Download and install Graphley for Mac", d), crumbs("Download", "/download/"), APP, ORG]
    rows = "\n".join(f'              <tr><td>{a}</td><td>{b}</td></tr>' for a, b in WHATS_NEW)
    h = head("/download/", "Download and install Graphley for Mac", d, graph) + header("/download/") + f'''  <main id="main">
    <div class="hero download-intro shell">
      <div class="download-head">
        <h1>Download Graphley <em>for Mac.</em></h1>
        <p class="lead">Every site and app in one calm chart. Every feature is free.</p>
      </div>

      <section class="download-support" aria-labelledby="download-support-title">
        <span class="support-icon" aria-hidden="true">{ICON_CHAT}</span>
        <h2 id="download-support-title">Free software. <span>Shaped by people.</span></h2>
        <p class="support-copy">Every Graphley feature is free, with nothing to unlock. Report a bug, suggest a source, or tell us how Graphley is working for you.</p>
        <div class="support-actions">
          <a class="button secondary" href="https://projectatom.ai/apps?app=graphley#feedback">{ICON_CHAT}Send Feedback <span aria-hidden="true">↗</span></a>
        </div>
      </section>

      <div class="download-get">
        <a class="button download-button" href="{DMG}" download>{APPLE.replace('width="16" height="16"', 'width="20" height="20"')}<span>Download Graphley {rel("version")}</span></a>
        <p class="fineprint">macOS 14 or later · Version {rel("version")} (build {rel("build")}) · {rel("size")}</p>
        <p class="fineprint">Code signed · Notarized by Apple · Signed automatic updates</p>
        <div class="testflight-get">
          {TF_BUTTON}
          <p class="fineprint">{TF_NOTE}</p>
        </div>
      </div>
    </div>

    <section class="shell download-guide" id="install" aria-labelledby="install-title">
      <h2 id="install-title">How to install Graphley</h2>
      <ol class="install-steps">
        <li><div><strong>Open the disk image.</strong><p>Open <code>Graphley-{REL["version"]}.dmg</code> in Downloads. Drag Graphley into Applications, then eject the disk&nbsp;image.</p></div></li>
        <li><div><strong>Launch Graphley from Applications.</strong><p>If macOS asks for confirmation, choose Open.</p></div></li>
        <li><div><strong>Connect Google Analytics.</strong><p>Sign in with Google. Graphley asks for read-only access, finds every GA4 property you can read and lets you pick the ones to track.</p></div></li>
        <li><div><strong>Add your apps, if you have any.</strong><p>Add an App Store Connect API key with access to Sales and Trends. It’s saved in the Keychain. Or connect an agent and let it do the setup: see <a href="/mcp/">MCP setup</a>.</p></div></li>
      </ol>
      <p><strong>Automatic updates.</strong> Graphley checks for new versions and installs signed updates for you. You can also choose <strong>Check for Updates</strong> from the Graphley menu.</p>
      <details class="download-verification">
        <summary>Verify your download</summary>
        <p>In Terminal, run <code>shasum -a 256 ~/Downloads/Graphley-{REL["version"]}.dmg</code> and compare the result with this SHA-256 checksum.</p>
        {rel("sha")}
      </details>
    </section>

    <section class="shell download-guide" id="whats-new" aria-labelledby="whats-new-title">
      <h2 id="whats-new-title">What’s in Graphley 0.1.0</h2>
      <div class="table-wrap">
        <table class="tide-table">
          <thead><tr><th>Part</th><th>What it does</th></tr></thead>
          <tbody>
{rows}
          </tbody>
        </table>
      </div>
      <p>The iPhone and iPad companion app is in beta on <a href="{TESTFLIGHT}" target="_blank" rel="noopener noreferrer">TestFlight</a>. It pairs with the Mac app and shows the same&nbsp;numbers.</p>
    </section>
  </main>
''' + footer(status=False)
    write("download/index.html", h)


TOOLS = [("get_status", "Which accounts are connected, how many sites, apps and dashboards there are, and when data was last refreshed."),
         ("list_sites · list_apps · list_dashboards", "What Graphley tracks today, with IDs to use in other tools."),
         ("query_metric", "Daily values for any metric, for one site or all of them, optionally by page or platform."),
         ("compare_periods", "The last N days against the N days before, per site, with percent change."),
         ("discover_ga4_properties", "Every GA4 property your Google account can read, marked tracked or not."),
         ("add_site · update_site · archive_site", "Track a website, change it, or stop tracking it (history is kept)."),
         ("add_app", "Track an App Store app by its Apple ID, linked to its website if you like."),
         ("create_dashboard · add_widget · remove_widget", "Build and change dashboards."),
         ("refresh_all", "Pull fresh numbers now."),
         ("set_app_store_key", "Save an App Store Connect key to the Keychain. Off unless you allow it."),
         ("set_source_key · set_google_service_account", "Save a Bing, X, Instagram, OpenTalon or Google service account key to the Keychain. Off unless you allow it."),
         ("record_followers · import_history", "Record a follower count for an account with no API, or bring in history from an older tracker."),
         ("list_reviews", "Written App Store reviews, with the day each was first seen."),
         ("export_backup", "The whole workspace and every stored number as one JSON file, for a backup. Keys are never included."),
         ("setup_portfolio", "Loads an example set of sites, apps and dashboards in one step.")]


def mcp():
    d = "How Graphley’s built-in MCP server lets Claude Code, Codex and Claude chat set up your sites, apps and dashboards."
    graph = [webpage("/mcp/", "MCP setup · Graphley", d), crumbs("MCP setup", "/mcp/"), APP, ORG]
    tools = "\n".join(f'              <tr><td><code>{n}</code></td><td>{t}</td></tr>' for n, t in TOOLS)
    h = head("/mcp/", "MCP setup · Graphley", d, graph) + header("/mcp/") + f'''  <main id="main">
    <div class="shell page-head">
      <span class="mark">mcp setup</span>
      <h1>Connect an agent to Graphley.</h1>
      <p class="lead">Graphley’s MCP server runs on your Mac, on the same data as the app. Install Graphley, add it to your agent, and ask for what you want tracked.</p>
    </div>
    <div class="shell doc">
      <nav class="toc" aria-label="On this page">
        <strong>On this page</strong>
        <a href="#how">How it works</a>
        <a href="#claude-code">Claude Code</a>
        <a href="#codex">Codex</a>
        <a href="#claude-chat">Claude chat</a>
        <a href="#tools">Tools</a>
        <a href="#try">Try it</a>
      </nav>
      <div class="prose">
        <section id="how">
          <h2>How it works</h2>
          <p>The Graphley app runs as an MCP server when your agent starts it with <code>--mcp</code>. It talks over standard input and output, on your Mac only, and reads and writes the same local workspace the app shows. Changes appear in the app right away and are listed under <strong>Settings → Agents</strong>.</p>
          <p class="note"><strong>You stay in control.</strong> Turn off <strong>Let agents make changes</strong> to keep agents view only. Saving keys is off unless you turn on <strong>Let agents set keys</strong>, and even then a key is read from the environment, never typed into a chat.</p>
        </section>
        <section id="claude-code">
          <h2>Claude Code</h2>
          <p>Add Graphley as a local server for your user or project:</p>
          <p class="prompt">claude mcp add graphley -- /Applications/Graphley.app/Contents/MacOS/Graphley --mcp</p>
        </section>
        <section id="codex">
          <h2>Codex</h2>
          <p>Add this to <code>~/.codex/config.toml</code>:</p>
          <p class="prompt">[mcp_servers.graphley]<br>command = "/Applications/Graphley.app/Contents/MacOS/Graphley"<br>args = ["--mcp"]</p>
        </section>
        <section id="claude-chat">
          <h2>Claude chat</h2>
          <p>In the Claude desktop app, open <strong>Settings → Developer → Edit Config</strong> and add a <code>graphley</code> entry under <code>mcpServers</code> with the same command and the <code>--mcp</code> argument. Restart Claude.</p>
        </section>
        <section id="tools">
          <h2>Tools</h2>
          <div class="table-wrap">
            <table class="tide-table">
              <thead><tr><th>Tool</th><th>What it does</th></tr></thead>
              <tbody>
{tools}
              </tbody>
            </table>
          </div>
        </section>
        <section id="try">
          <h2>Try it</h2>
          <p class="prompt">Find my Google Analytics properties and track the ones that aren’t in Graphley yet.</p>
          <p class="prompt">Make a Launch dashboard with visitors per day and App Store downloads for my newest app.</p>
          <p class="prompt">Which site grew the most this month, and which pages drove it?</p>
        </section>
      </div>
    </div>
  </main>
''' + footer(status=False)
    write("mcp/index.html", h)


FAQ = [("What is Graphley?", "Graphley is a free analytics app for Mac, from Project ATOM. It puts every website and App Store app you run in one dashboard, using Google Analytics 4 and App Store Connect, with no Graphley server. Your AI agents can set it up through its built-in MCP server."),
       ("How do I get it?", "Download the signed and notarized disk image from graphley.ai/download, open it and drag Graphley into Applications. It needs macOS 14 or later."),
       ("Is it free?", "Yes. Graphley is free and source available, with no account, no trial and nothing to unlock."),
       ("How does it update?", "Graphley checks for new versions and installs signed updates automatically. You can also choose Check for Updates from the Graphley menu."),
       ("Is there an iPhone app?", f"Yes, in beta. Join the iPhone and iPad beta on TestFlight at {TESTFLIGHT}. It shows the same numbers as your Mac, synced through your own private iCloud database."),
       ("Which sources does it read?", "Google Analytics 4 for websites, App Store Connect sales reports for app downloads, App Store ratings and reviews in every storefront, Google Search Console and Bing Webmaster Tools for search, and follower counts from X, Instagram, YouTube and GitHub (Substack and LinkedIn by hand)."),
       ("Where is my data kept?", "On your Mac. Graphley has no server. Sign-in tokens and keys stay in the Keychain."),
       ("Which AI agents can work with Graphley?", "Claude Code, Codex and Claude chat, through a local MCP server with 23 tools. You choose whether agents can only view, or can also make changes.")]


def help_page():
    d = "Answers about Graphley for Mac: installing, updates, sources, privacy and agents, and how to reach us."
    faq = {"@type": "FAQPage", "@id": f"{SITE}/help/#faq", "url": f"{SITE}/help/",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    graph = [webpage("/help/", "Help · Graphley", d), faq, crumbs("Help", "/help/"), APP, ORG]
    qa = "\n".join(f"          <h3>{q}</h3>\n          <p>{a}</p>" for q, a in FAQ)
    h = head("/help/", "Help · Graphley", d, graph) + header() + f'''  <main id="main">
    <div class="shell page-head">
      <span class="mark">help</span>
      <h1>Graphley Help</h1>
      <p class="lead">{d}</p>
    </div>
    <div class="shell doc">
      <nav class="toc" aria-label="On this page">
        <strong>On this page</strong>
        <a href="#questions">Common questions</a>
        <a href="#contact">Get in touch</a>
      </nav>
      <div class="prose">
        <section id="questions">
          <h2>Common questions</h2>
{qa}
        </section>
        <section id="contact">
          <h2>Get in touch</h2>
          <p>Ask a question or tell us what you’d like Graphley to track in <a href="https://projectatom.ai/apps?app=graphley#feedback">our Send feedback</a>, or send feedback with <a href="https://projectatom.ai/apps?app=graphley#feedback">our feedback form</a>.</p>
        </section>
      </div>
    </div>
  </main>
''' + footer(status=False)
    write("help/index.html", h)


def privacy():
    d = "How Graphley, its agent connections and this website handle information."
    graph = [webpage("/privacy/", "Privacy · Graphley", d), crumbs("Privacy", "/privacy/"), ORG]
    h = head("/privacy/", "Privacy · Graphley", d, graph) + header() + '''  <main id="main">
    <div class="shell page-head">
      <span class="mark">privacy</span>
      <h1>Privacy</h1>
      <p class="lead">Graphley is a Project ATOM project. Your numbers stay on your devices. Updated November 27, 2026.</p>
    </div>
    <div class="shell doc single">
      <div class="prose">
        <section>
          <h2>The app</h2>
          <p>Graphley stores your workspace (the sites, apps and dashboards you set up) and the numbers it fetches on your Mac. It fetches them directly from the services you connect, using your own sign-in and keys: Google Analytics, Google Search Console, App Store Connect, Bing Webmaster Tools and Instagram. It also reads public App Store listings and public YouTube channel feeds for the apps and channels you add. Graphley has no server and no account, and sends nothing to us.</p>
          <p>Sign-in tokens and keys are kept in the Keychain. If you use iCloud Keychain, they are available on your other Macs.</p>
          <p>To check for updates, Graphley downloads a small feed from graphley.ai. The request carries the app and macOS version, as any web request does, and no analytics data.</p>
        </section>
        <section>
          <h2>iPhone and iCloud</h2>
          <p>When you use the iPhone and iPad app, the Mac writes a snapshot of your numbers to your private iCloud database so your iPhone can show them. Only you can read it. Keys and tokens are never part of the snapshot.</p>
        </section>
        <section id="mcp">
          <h2>Local agent connections</h2>
          <p>The MCP server runs on your Mac when an agent starts it, and works on the same local workspace. You choose whether agents can only view, or can also make changes, and whether they can save keys. Changes made by agents are listed in Settings → Agents.</p>
          <p>Your chosen agent may send information it retrieves to its AI provider. Review that provider’s privacy terms before connecting.</p>
        </section>
        <section>
          <h2 id="hosting">Where we host</h2>
          <p>This site runs on <a href="https://www.cloudflare.com/">Cloudflare</a>. Cloudflare serves every page and manages our traffic, so it handles standard request details such as your IP address and browser to deliver the site and protect it from abuse. Our images and downloads are stored in Cloudflare R2. Cloudflare handles that data under its <a href="https://www.cloudflare.com/privacypolicy/">privacy policy</a>.</p>
          <p>We&rsquo;re not a Cloudflare sponsor. We chose them because we think they&rsquo;re the best value and the best service, and we&rsquo;ll keep using them for as long as that stays true.</p>
        </section>
        <section id="website">
          <h2>This website</h2>
          <p>graphley.ai has no sign-up form and no account. If you click Allow analytics, the site loads Google Analytics, which sets cookies to count visits, page views and link clicks. Page addresses are sent without query strings, and advertising features are off. If you decline, Google Analytics does not load. Change your choice any time with Analytics settings in the footer.</p>
        </section>
        <section id="feedback">
          <h2>Feedback and support</h2>
          <p>Help and feedback for Graphley go through the <a href="https://projectatom.ai/apps?app=graphley#feedback">feedback form at projectatom.ai</a>. We receive the app you pick, your message and, only if you add it, your email address. The note is emailed to our team through Cloudflare Email. If you leave an email, we use it to reply and follow up. If you leave it out, we can’t reply.</p>
          <p>The app never sends a report on its own. Only what you type into the form is sent, so please leave private files and details out of it.</p>
        </section>
        <section id="contact">
          <h2>Questions and changes</h2>
          <p>We don’t sell your information, and we don’t use it for advertising. To ask what we hold, or to have it corrected or deleted, email <a href="mailto:hello@projectatom.ai">hello@projectatom.ai</a> or use the feedback form. We answer within 30 days.</p>
          <p>If this page changes, the date at the top changes with it.</p>
        </section>
      </div>
    </div>
  </main>
''' + footer(status=False)
    write("privacy/index.html", h)


def terms():
    t = "Terms · Graphley"
    d = "The terms for using Graphley, a free, public domain app from Project ATOM, and this website."
    graph = [webpage("/terms/", t, d), crumbs("Terms", "/terms/"), ORG]
    h = head("/terms/", t, d, graph) + header() + '''  <main id="main">
    <div class="shell page-head">
      <span class="mark">terms</span>
      <h1>Terms</h1>
      <p class="lead">Plain terms for a free app. Updated November 27, 2026.</p>
    </div>
    <div class="shell doc single">
      <div class="prose">
        <section>
          <h2>Using Graphley</h2>
          <p>Graphley is a free app from Project ATOM for Mac, iPhone and iPad. There is no account to make, nothing to buy and no ads. We share it as a signed download for Mac and through Apple’s TestFlight, and Apple’s own terms apply to anything you get through Apple. By using Graphley or this website, you agree to these terms.</p>
        </section>
        <section id="license">
          <h2>Public domain</h2>
          <p>Graphley’s code is free and open source, released into the public domain under the <a href="https://unlicense.org/">Unlicense</a>. Anyone may copy, change, share or sell it, for any purpose, without asking. We claim no copyright in it. Parts made by others, such as open source libraries, keep their own licenses.</p>
        </section>
        <section>
          <h2>Your work is yours</h2>
          <p>Your dashboards, settings and the numbers Graphley fetches for you belong to you. We don’t claim any rights in them, and using Graphley doesn’t give us any.</p>
        </section>
        <section>
          <h2>Use it kindly</h2>
          <p>Please don’t use Graphley to break the law, to harm, harass or deceive anyone, to send spam, or to get around the security of Graphley or any other service.</p>
        </section>
        <section>
          <h2>Services you connect</h2>
          <p>Some features work with services you choose, such as iCloud, Google Analytics, Search Console, App Store Connect, Bing Webmaster Tools, YouTube, Instagram or an AI agent on your Mac. Each of them has its own terms and privacy policy, and they apply when you use them through Graphley.</p>
        </section>
        <section>
          <h2>No warranty</h2>
          <p>We build Graphley with care, but it comes as is, with no warranty of any kind. We can’t promise it will always work, be available, or be free of mistakes. Numbers come from the services you connect, and they can be late or incomplete. To the fullest extent the law allows, we aren’t liable for any loss or damage that comes from using it, including lost data, so keep backups of anything that matters to you. Nothing here takes away rights the law gives you that can’t be waived.</p>
        </section>
        <section>
          <h2>Changes and contact</h2>
          <p>If these terms change, the date at the top changes with them. For questions, use the <a href="https://projectatom.ai/apps?app=graphley#feedback">feedback form</a> or email <a href="mailto:hello@projectatom.ai">hello@projectatom.ai</a>. Our <a href="/privacy/">privacy page</a> explains how Graphley handles information.</p>
        </section>
      </div>
    </div>
  </main>
''' + footer()
    write("terms/index.html", h)


def notfound():
    h = head("/404", "Page not found · Graphley", "", None, noindex=True) + header(body_class="missing-page") + f'''  <main id="main" class="hero missing-hero shell">
    <img src="/assets/icon.png?v=20261124" width="66" height="66" alt="">
    <h1>Page <em>not found.</em></h1>
    <p class="lead">The page may have moved. You can still get back to Graphley or find help.</p>
    <div class="actions">
      <a class="button" href="/">{ICON_HOME}Back to Home</a>
      <a class="button secondary" href="/help/">{ICON_HELP}Get Help</a>
    </div>
  </main>
''' + footer(status=False)
    write("404.html", h)


index(); download(); mcp(); help_page(); privacy(); terms(); notfound()
print("ok", REL)
