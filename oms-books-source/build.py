#!/usr/bin/env python3
"""Builds the OMS Books static site into ./dist. Edit content here, then run: python3 build.py"""
import json, os, shutil, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, 'dist')

SITE = 'https://omnimediasyndicatedbooks.com'
EMAIL = 'submissions@omnimedia-books.com'
PHONE = '(415) 918-6468'
PHONE_TEL = '+14159186468'
VIDEO_MP4 = 'https://d8j0ntlcm91z4.cloudfront.net/user_34zVcIhIsOTW0q6TlxKlFv5n3Up/hf_20260922_190824_48a4aa6c-8635-4126-8d19-e55cad300211.mp4'
VIDEO_POSTER = 'https://d2ol7oe51mr4n9.cloudfront.net/user_34zVcIhIsOTW0q6TlxKlFv5n3Up/8254257b-bc02-4a9b-bbb4-49ea7233635e_resize.jpg'
CHLOE_IMG = 'https://d8j0ntlcm91z4.cloudfront.net/user_34zVcIhIsOTW0q6TlxKlFv5n3Up/hf_20260922_150503_2fa3aa24-2bce-4b39-ae2c-f88e059211f2_min.webp'

# ---------------------------------------------------------------- books
BOOKS = [
    dict(slug='vowed-to-love-a-hood-demon', title='Vowed to Love a Hood Demon', author='Diorr Monáe',
         genre='An Arranged Marriage Love Story', series=None, kicker='Arranged Marriage',
         blurb=[
             'They dressed Harmony Saint Clair in black lace and called it a wedding.',
             'Eleven days ago she was engaged to a preacher’s son. Then her father confessed what he owes the Duvernay family, a debt from 1999 that no amount of money can settle, and the price became his daughter.',
             'Now she’s married to Messiah Duvernay, the heir the streets call Menace, for one public year while a war with Miami heats up.',
             'Her terms: separate wings, her own work, and his hands to himself. His one rule: no lies under his roof.',
             'She swore she would never love him. He never planned to ask.',
             'The vows were the easy part.']),
    dict(slug='forged-vows', title='Forged Vows', author='Vienna Laurent',
         genre='A Dark Marriage Romance', series='The Voss Duet, Book One', kicker='Dark Romance',
         blurb=[
             'Nadia Cortez’s father died owing $286,000 to men who don’t send invoices. Her brake line is cut. Her storeroom burns. Then a card lands on her counter: VOSS.',
             'Damon Voss offers a way out: one year of marriage, the debt cleared at signing, separate lives. Nadia wins five terms of her own, including the one that matters most. Lie to me once, and I walk.',
             'She doesn’t read item thirty-one closely enough.',
             'Damon didn’t marry her for love. He married her for what her father hid, and for what her father saw the morning Damon’s mother fell from a roof.',
             'The con is working. The problem is, he’s falling for his mark.']),
    dict(slug='the-second-mrs-brandt', title='The Second Mrs. Brandt', author='Marnie Callister',
         genre='A Psychological Thriller', series='The Heron Court Duology, Book One', kicker='Psychological Thriller',
         blurb=[
             'Cara arrives at the Brandt estate with three hundred dollars and nowhere else to go. Elliott Brandt hires her on the spot, for far more money than the job should pay.',
             'The house has rules. Closed rooms. A six-year-old who won’t speak. A wife who is “traveling.”',
             'And every night, footsteps overhead in a house Elliott swears is empty.',
             'Cara found the diary. She found the death certificate. She was sure she knew which Brandt to fear.',
             'She was wrong about everything except the footsteps.']),
    dict(slug='seven-nights-at-sea', title='Seven Nights at Sea', author='Lainey Beckett',
         genre='A Romantic Comedy', series='The Cabin 734 Duet, Book One', kicker='Romantic Comedy',
         blurb=[
             'Margo booked a seven-night singles cruise with a laminated itinerary and one goal: prove she’s over the man who walked out three years ago without a word.',
             'Then she opens cabin 734 and finds Liam standing in it.',
             'One cabin. One bed. A booking error guest services swears they can’t fix. They draw a line down the middle of the mattress and agree on rules: no touching, no questions about the past.',
             'Seven nights is a long time to keep rules.',
             'And Liam didn’t board this ship by accident.']),
]

# ---------------------------------------------------------------- FAQ (also powers Chloe)
FAQ = [
    dict(q='Is it free to get published with OMS Books?', chip=True,
         keys=['free', 'cost', 'charge', 'pay', 'fee', 'price', 'expensive'],
         a='Yes. Authors we sign pay nothing to be published. We handle editing, cover design, formatting, and distribution in paperback, ebook, and audiobook. Our <a href="/boutique/">boutique services</a> are separate and paid, for authors who want to publish on their own and keep all their rights.'),
    dict(q='Who qualifies for the six-figure signing bonus?', chip=True,
         keys=['bonus', 'six figure', 'six-figure', '100', 'qualify', 'signing money', 'advance'],
         a='The signing bonus is for experienced authors with multiple published books and a completed manuscript ready for publication. Bonus eligibility, amount, and timing are set case by case, and not every applicant qualifies. <a href="/submit/?path=bonus">Apply for bonus consideration</a>.'),
    dict(q='What’s the difference between getting signed and boutique services?', chip=True,
         keys=['difference', 'boutique', 'signed', 'rights', 'keep my rights', 'self publish', 'self-publish', 'package'],
         a='When we sign you, OMS Books publishes your book at no cost to you, under an agreement you review before signing. Boutique services are for authors publishing on their own: you keep every right and hire us only for what you need, like editing, ghostwriting, or a cover.'),
    dict(q='What formats do you publish?', chip=True,
         keys=['format', 'paperback', 'ebook', 'e-book', 'audio', 'kindle', 'print', 'hardcover'],
         a='Every book we sign is published in paperback, ebook, and audiobook.'),
    dict(q='Will my book be made into a film?', chip=True,
         keys=['film', 'movie', 'vertical', 'screen', 'video', 'adapt', 'tv', 'series'],
         a='Film isn’t guaranteed. Our top-selling titles may be considered for vertical film adaptation and further screen development. Read more on our <a href="/page-to-screen/">Page to Screen</a> page.'),
    dict(q='How do I submit my manuscript?', chip=True,
         keys=['submit', 'send', 'apply', 'manuscript', 'query', 'how do i start', 'get started', 'sign up'],
         a='Fill out our <a href="/submit/">submission form</a> with a short summary of your book. Our team reviews submissions within 24 to 48 hours.'),
    dict(q='Do I need a finished manuscript?', chip=False,
         keys=['finished', 'complete', 'unfinished', 'idea', 'draft', 'not done', 'halfway'],
         a='For the signing bonus, yes. For everything else, send what you have and we’ll recommend a path. If you’re starting from an idea, our boutique ghostwriting and editing services can help you get to a finished book.'),
    dict(q='What genres do you publish?', chip=False,
         keys=['genre', 'romance', 'thriller', 'fiction', 'nonfiction', 'non-fiction', 'fantasy', 'urban', 'mystery'],
         a='Our launch slate covers romance, from dark romance to romantic comedy, and psychological thrillers. Whatever you write, send it in and we’ll take a look.'),
    dict(q='Where are you located?', chip=False,
         keys=['where', 'located', 'location', 'atlanta', 'office', 'address'],
         a='OMS Books is based in Atlanta, Georgia, and works with authors across the United States.'),
    dict(q='How do I contact you?', chip=False,
         keys=['contact', 'email', 'phone', 'call', 'talk', 'human', 'person', 'reach'],
         a='Email us at <a href="mailto:%s">%s</a>, call <a href="tel:%s">%s</a>, or use the <a href="/submit/">submission form</a>.' % (EMAIL, EMAIL, PHONE_TEL, PHONE)),
    dict(q='How do I hear about new releases?', chip=False,
         keys=['newsletter', 'mailing', 'list', 'release', 'updates', 'notify', 'coming soon', 'when'],
         a='Join our <a href="#newsletter">mailing list</a> and you’ll be the first to know when covers, release dates, and preorders go live.'),
]

NAV = [('/books/', 'Books'), ('/get-signed/', 'Get Signed'), ('/boutique/', 'Boutique'),
       ('/page-to-screen/', 'Page to Screen'), ('/about/', 'About'), ('/faq/', 'FAQ')]

ARROW = '<span class="arr" aria-hidden="true">&rarr;</span>'

def e(s):
    return html.escape(s, quote=True)

def head(title, desc, path):
    full = title if title.startswith('OMS Books') else '%s | OMS Books' % title
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta name="theme-color" content="#030712">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/anton.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

def header(path):
    cur = ' aria-current="page"'
    links = ''.join(
        f'<a href="{href}"{cur if path.startswith(href) else ""}>{label}</a>' for href, label in NAV)
    return f'''<div class="ticker" role="note"><span>Now signing authors</span><span class="dot" aria-hidden="true">&#9679;</span><span>No fees to sign</span><span class="dot" aria-hidden="true">&#9679;</span><span>Paperback &middot; eBook &middot; Audiobook</span></div>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/" aria-label="OMS Books home">OMS<span>/</span>BOOKS</a>
    <button class="menu-btn" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Open menu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
    <nav class="nav" id="site-nav" aria-label="Main">{links}<a class="btn btn-blue" href="/submit/">Submit</a></nav>
  </div>
</header>
'''

def bonus_band():
    return f'''<section class="bonus-band" aria-labelledby="bonus-h">
  <div class="wrap">
    <div>
      <p class="eyebrow">For experienced authors</p>
      <h2 class="display" id="bonus-h">Up to a six-figure signing bonus</h2>
    </div>
    <div>
      <p>For authors with multiple published books and a completed manuscript. Bonus eligibility, amount, and timing are set case by case.</p>
      <a class="btn btn-white" href="/submit/?path=bonus">See if you qualify {ARROW}</a>
    </div>
  </div>
</section>
'''

def video_bonus_hero():
    return f"""<section class="vhero" aria-labelledby="bonus-h">
  <div class="wrap">
    <div>
      <p class="eyebrow">For experienced authors</p>
      <h2 class="display" id="bonus-h">Up to a six-figure<br><span class="blue-l">signing bonus</span></h2>
      <p class="vhero-sub">For authors with multiple published books and a completed manuscript. Bonus eligibility, amount, and timing are set case by case.</p>
      <div class="vhero-cta">
        <a class="btn btn-blue" href="/submit/?path=bonus">See if you qualify {ARROW}</a>
        <a class="btn btn-ghost" href="/get-signed/">Get signed free {ARROW}</a>
      </div>
    </div>
    <figure class="hero-video" style="margin:0">
      <video src="{VIDEO_MP4}" poster="{VIDEO_POSTER}" autoplay muted loop playsinline controls preload="metadata" width="340" height="604" aria-label="OMS Books 30-second introduction"></video>
      <figcaption class="cap"><span>Why traditional publishing is dead</span><span>0:30</span></figcaption>
    </figure>
  </div>
</section>
"""

def newsletter(heading='Be first to read.', text='Cover reveals, release dates, and preorder links for every new OMS book, straight to your inbox.'):
    return f'''<section class="news" id="newsletter" aria-labelledby="news-h">
  <div class="wrap">
    <div>
      <h2 class="display" id="news-h">{heading}</h2>
      <p>{text}</p>
    </div>
    <form class="news-form" name="newsletter" method="POST" action="/thank-you/?form=newsletter" data-netlify="true" netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="newsletter">
      <p class="hp"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
      <label class="sr-only" for="nl-name">First name</label>
      <input id="nl-name" type="text" name="first-name" placeholder="First name" autocomplete="given-name">
      <div class="inline">
        <label class="sr-only" for="nl-email">Email address</label>
        <input id="nl-email" type="email" name="email" placeholder="Email address" required autocomplete="email">
        <button class="btn" type="submit">Join the list {ARROW}</button>
      </div>
      <p class="fine">No spam. Unsubscribe anytime.</p>
    </form>
  </div>
</section>
'''

def footer():
    return f'''<footer class="site-footer">
  <div class="wrap">
    <p class="foot-big">Write it.<br><span>We&rsquo;ll publish it.</span></p>
    <div class="foot-cols">
      <div>
        <a class="logo" href="/" style="color:#fff">OMS<span>/</span>BOOKS</a>
        <p style="margin-top:16px">OmniMedia Syndicated Books publishes in paperback, ebook, and audiobook. Atlanta, Georgia.</p>
      </div>
      <div>
        <h4>Authors</h4>
        <ul><li><a href="/get-signed/">Get signed</a></li><li><a href="/get-signed/#bonus">Signing bonus</a></li><li><a href="/boutique/">Boutique services</a></li><li><a href="/submit/">Submit</a></li></ul>
      </div>
      <div>
        <h4>Readers</h4>
        <ul><li><a href="/books/">Books</a></li><li><a href="/page-to-screen/">Page to Screen</a></li><li><a href="/#newsletter">Mailing list</a></li><li><a href="/faq/">FAQ</a></li></ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="tel:{PHONE_TEL}">{PHONE}</a></li><li><a href="/about/">About</a></li></ul>
      </div>
    </div>
    <div class="foot-base">
      <span>&copy; 2026 OmniMedia Syndicated Books</span>
      <span><a href="/privacy-policy/">Privacy</a> &middot; <a href="/terms-and-conditions/">Terms</a> &middot; <a href="/refund-policy/">Refunds</a></span>
    </div>
  </div>
</footer>
'''

def chat():
    return f'''<div class="chat-launch" id="chat-launch" aria-expanded="false">
  <button class="chat-bubble" type="button" aria-controls="chat-panel">Questions? Ask Chloe.</button>
  <button class="chat-avatar-btn" type="button" aria-controls="chat-panel" aria-label="Chat with Chloe">
    <img src="{CHLOE_IMG}" alt="" width="68" height="68" loading="lazy"><span class="live" aria-hidden="true"></span>
  </button>
</div>
<section class="chat-panel" id="chat-panel" role="dialog" aria-label="Chat with Chloe">
  <div class="chat-head">
    <img src="{CHLOE_IMG}" alt="Chloe" width="48" height="48" loading="lazy">
    <div class="who"><strong>Chloe</strong><span>OMS Books assistant</span></div>
    <button class="chat-close" type="button" aria-label="Close chat"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
  </div>
  <div class="chat-log" aria-live="polite"></div>
  <form class="chat-form">
    <label class="sr-only" for="chat-q">Your question</label>
    <input id="chat-q" type="text" placeholder="Ask Chloe a question" autocomplete="off">
    <button type="submit" aria-label="Send"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
  </form>
</section>
<script src="/assets/js/faq-data.js"></script>
<script src="/assets/js/site.js"></script>
'''

def page(path, title, desc, body, news=True):
    out = head(title, desc, path) + header(path) + '<main id="main">\n' + body
    if news:
        out += newsletter()
    out += '</main>\n' + footer() + chat() + '</body>\n</html>\n'
    return out

def book_card(b):
    return f'''<a class="book-card" href="/books/#{b['slug']}">
  <div class="cover"><img src="/assets/covers/{b['slug']}.jpg" alt="Cover of {e(b['title'])} by {e(b['author'])}" width="800" height="1192" loading="lazy"></div>
  <span class="kicker">Coming soon &middot; {e(b['kicker'])}</span>
  <span class="title">{e(b['title'])}</span>
  <span class="by">by {e(b['author'])}</span>
</a>'''

def steps():
    items = [('01', 'Submit', 'Send your manuscript summary through our form.'),
             ('02', 'Sign', 'Accepted authors sign with OMS Books at no cost.'),
             ('03', 'Publish', 'Edited, designed, and released in paperback, ebook, and audiobook.'),
             ('04', 'Grow', 'Marketing behind every launch. Top sellers are considered for film.')]
    return '<div class="steps">' + ''.join(
        f'<div class="step"><span class="num">{n}</span><h3>{t}</h3><p>{d}</p></div>' for n, t, d in items) + '</div>'

# ---------------------------------------------------------------- pages
def home():
    cards = '\n'.join(book_card(b) for b in BOOKS)
    body = video_bonus_hero() + f'''<section class="hero wrap" aria-labelledby="hero-h">
  <div class="meta-row"><span>Vol. 01</span><span>Paperback &middot; eBook &middot; Audiobook</span><span>Est. 2026</span></div>
  <h1 class="display" id="hero-h">Your book.<br><span class="blue">Published.</span></h1>
  <div class="hero-grid">
    <p class="lede">OMS Books signs authors at no cost and publishes their work in paperback, ebook, and audiobook.</p>
    <p>Our top sellers can go further. Select titles are developed into vertical films and pitched for the screen.</p>
    <div class="stack">
      <a class="btn btn-ink" href="/get-signed/">Get signed free {ARROW}</a>
      <a class="btn" href="/boutique/">Boutique services {ARROW}</a>
    </div>
  </div>
</section>
<div class="wrap">
  <div class="proof">
    <div><span class="display">Amazon bestsellers</span><span class="eyebrow">Launched by our team</span></div>
    <div><span class="display blue">500,000+</span><span class="eyebrow">Followers in our promotional network</span></div>
    <div><span class="display">3 formats</span><span class="eyebrow">Paperback &middot; eBook &middot; Audiobook</span></div>
  </div>
</div>
<div style="height:64px"></div>
<section class="paths" aria-label="Two ways to work with us">
  <div class="path path-ink">
    <p class="eyebrow">Path 01 &middot; Free</p>
    <h2 class="display">Get signed</h2>
    <p>No fees. We edit, design, publish, and distribute your book in paperback, ebook, and audiobook.</p>
    <a class="btn btn-white" href="/get-signed/">How signing works {ARROW}</a>
  </div>
  <div class="path path-blue">
    <p class="eyebrow">Path 02 &middot; Pay as you go</p>
    <h2 class="display">Boutique</h2>
    <p>Keep every right. Hire us for the piece you need: editing, ghostwriting, covers, formatting.</p>
    <a class="btn btn-white" href="/boutique/">See services {ARROW}</a>
  </div>
</section>
<section class="section wrap" aria-labelledby="slate-h">
  <div class="section-head"><h2 class="display" id="slate-h">On the slate</h2><a href="/books/">All books &rarr;</a></div>
  <div class="book-row">
{cards}
  </div>
</section>
<section class="wrap" style="padding-bottom:88px" aria-labelledby="how-h">
  <div class="section-head"><h2 class="display" id="how-h">How it works</h2><a href="/submit/">Start now &rarr;</a></div>
  {steps()}
</section>
'''
    return page('/', 'OMS Books | Get Published. Get Paid. Get Seen.',
                'OMS Books signs authors free and publishes in paperback, ebook, and audiobook. Experienced authors may qualify for up to a six-figure signing bonus.', body)

def books():
    items = []
    for b in BOOKS:
        paras = ''.join(f'<p>{e(p)}</p>' for p in b['blurb'])
        series = f'<span class="chip">{e(b["series"])}</span>' if b['series'] else ''
        items.append(f'''<article class="book-item" id="{b['slug']}">
  <div class="cover"><img src="/assets/covers/{b['slug']}.jpg" alt="Cover of {e(b['title'])} by {e(b['author'])}" width="800" height="1192" loading="lazy"></div>
  <div>
    <p class="eyebrow blue">{e(b['genre'])}</p>
    <h2 class="display">{e(b['title'])}</h2>
    <p class="by">by {e(b['author'])}</p>
    <div class="blurb">{paras}</div>
    <div class="formats"><span class="chip chip-blue">Coming soon</span><span class="chip">Paperback</span><span class="chip">eBook</span><span class="chip">Audiobook</span>{series}</div>
    <a class="btn btn-ink" href="#newsletter">Get release alerts {ARROW}</a>
  </div>
</article>''')
    body = f'''<section class="page-hero wrap">
  <p class="eyebrow">The OMS catalog</p>
  <h1 class="display">Books</h1>
  <p class="lede">Our launch slate. Every title arrives in paperback, ebook, and audiobook.</p>
</section>
<section class="section wrap"><div class="book-list">
{''.join(items)}
</div></section>
'''
    return page('/books/', 'Books', 'New romance and psychological thrillers from OMS Books, coming soon in paperback, ebook, and audiobook.', body)

def get_signed():
    body = f'''<section class="page-hero wrap">
  <p class="eyebrow">Path 01 &middot; Free</p>
  <h1 class="display">Get signed</h1>
  <p class="lede">Authors we sign pay nothing to be published. You write. We handle everything it takes to put your book in readers&rsquo; hands.</p>
</section>
<section class="section wrap">
  <div class="section-head"><h2 class="display">What you get</h2></div>
  <div class="service-grid">
    <div class="service"><h3>Editing</h3><p>Professional editors refine your manuscript for structure, clarity, and polish.</p></div>
    <div class="service"><h3>Cover design</h3><p>A market-ready cover built to stop the scroll in your genre.</p></div>
    <div class="service"><h3>Formatting</h3><p>Interior layout and publication-ready files for print and digital.</p></div>
    <div class="service"><h3>Three formats</h3><p>Your book released in paperback, ebook, and audiobook.</p></div>
    <div class="service"><h3>Distribution</h3><p>Placement with major online retailers and digital platforms.</p></div>
    <div class="service"><h3>Marketing</h3><p>Launch support and promotion through our 500,000+ follower network.</p></div>
  </div>
  <p class="fine" style="margin-top:20px">Top-selling titles may also be considered for vertical film adaptation. <a href="/page-to-screen/">Learn about Page to Screen</a>.</p>
</section>
<section class="wrap" id="bonus" style="scroll-margin-top:110px">
  <div class="callout">
    <p class="eyebrow">For experienced authors</p>
    <h2 class="display">Up to a six-figure signing bonus</h2>
    <p style="font-size:20px;max-width:760px;margin:0">Established authors bring an audience with them, and we pay for it. Qualifying authors may receive a signing bonus of up to six figures, paid when the contract is signed.</p>
    <div class="cols" style="margin-top:12px">
      <div>
        <h3 class="eyebrow" style="margin-bottom:14px">To qualify, you need</h3>
        <ul style="margin:0;padding-left:20px;font-size:18px">
          <li>Multiple books already published</li>
          <li>A completed manuscript ready for publication</li>
          <li>A story that fits our multi-format publishing model</li>
        </ul>
      </div>
      <div style="display:flex;flex-direction:column;gap:16px;justify-content:flex-end">
        <a class="btn btn-blue" href="/submit/?path=bonus">Apply for bonus consideration {ARROW}</a>
        <p class="fine" style="margin:0">Bonus eligibility, amount, and timing are determined case by case. Not all applicants qualify.</p>
      </div>
    </div>
  </div>
</section>
<section class="section wrap">
  <div class="section-head"><h2 class="display">The process</h2><a href="/submit/">Submit &rarr;</a></div>
  {steps()}
</section>
'''
    return page('/get-signed/', 'Get Signed', 'Get published by OMS Books at no cost. Experienced authors may qualify for up to a six-figure signing bonus.', body)

def boutique():
    services = [('Editing', 'Developmental, line, and copy editing, matched to where your draft is right now.'),
                ('Ghostwriting', 'Have the idea but not the time? Our writers bring your story to the page in your voice.'),
                ('Cover design', 'Genre-smart covers that look at home next to the bestsellers.'),
                ('Formatting', 'Clean interior layout and files ready for print and ebook platforms.'),
                ('Audiobook production', 'Turn your finished book into an audiobook listeners can find.'),
                ('Marketing', 'Launch plans, social content, and promotion built around your book.')]
    grid = ''.join(f'<div class="service"><h3>{t}</h3><p>{d}</p></div>' for t, d in services)
    body = f'''<section class="page-hero wrap">
  <p class="eyebrow">Path 02 &middot; Pay as you go</p>
  <h1 class="display">Boutique</h1>
  <p class="lede">Publishing on your own terms? Keep every right and hire us only for what you need.</p>
</section>
<section class="section wrap">
  <div class="section-head"><h2 class="display">Services</h2><a href="/submit/?path=boutique">Request a quote &rarr;</a></div>
  <div class="service-grid">{grid}</div>
</section>
<section class="wrap" style="padding-bottom:88px">
  <div class="cols">
    <h2>You keep your rights.</h2>
    <div class="prose">
      <p>Boutique clients publish under their own name. You pay for the services you choose, and the book and its rights stay yours.</p>
      <p>Not sure what you need? Tell us where your book is and we&rsquo;ll put together a package.</p>
      <a class="btn btn-ink" href="/submit/?path=boutique">Request a quote {ARROW}</a>
    </div>
  </div>
</section>
'''
    return page('/boutique/', 'Boutique Services', 'Editing, ghostwriting, cover design, formatting, and audiobook production for authors who keep their rights.', body)

def page_to_screen():
    body = f'''<section class="page-hero wrap">
  <p class="eyebrow">For our top sellers</p>
  <h1 class="display">Page to screen</h1>
  <p class="lede">Every OMS book is published first. The ones readers can&rsquo;t put down can go further.</p>
</section>
<section class="section wrap">
  <div class="cols">
    <h2>Vertical films</h2>
    <div class="prose">
      <p>Readers discover stories on their phones. For select top-selling titles, OMS produces vertical films built for short-form video platforms, bringing a book&rsquo;s characters and biggest moments to the feed.</p>
      <p>A strong vertical film series can grow a book&rsquo;s audience and build the case for a larger screen adaptation. When a story earns it, we take it further.</p>
    </div>
  </div>
</section>
<section class="wrap" style="padding-bottom:88px">
  <div class="callout">
    <p class="eyebrow">Straight talk</p>
    <h2 class="display">Film isn&rsquo;t guaranteed</h2>
    <p style="font-size:20px;max-width:760px;margin:0">Screen development is reserved for our top-selling titles, and we decide case by case. Publishing is our promise to every author we sign. Film is an opportunity some books earn.</p>
    <div><a class="btn btn-blue" href="/get-signed/">Start with publishing {ARROW}</a></div>
  </div>
</section>
'''
    return page('/page-to-screen/', 'Page to Screen', 'OMS Books develops select top-selling titles into vertical films and pitches them for the screen.', body)

def about():
    body = f'''<section class="page-hero wrap">
  <p class="eyebrow">About OMS Books</p>
  <h1 class="display">Built for authors</h1>
  <p class="lede">OmniMedia Syndicated Books is a publishing house for a new generation of writers, based in Atlanta, Georgia.</p>
</section>
<section class="section wrap">
  <div class="cols">
    <h2>What we do</h2>
    <div class="prose">
      <p>Today&rsquo;s writers need more than editing and distribution. They need visibility, an audience, and a team that knows how to position a book in a digital world.</p>
      <p>We sign authors at no cost and publish their books in paperback, ebook, and audiobook. For authors who want to keep their rights, our boutique services offer editing, ghostwriting, cover design, and more, one piece at a time.</p>
      <p>Our team has launched Amazon bestsellers and runs a promotional network of more than 500,000 followers. Our strongest titles can go further, into vertical film and development for the screen.</p>
      <h2>Our mission</h2>
      <p>To help great stories reach the readers they deserve, and to build real careers around the people who write them.</p>
      <h2>Get in touch</h2>
      <p>Email <a href="mailto:{EMAIL}">{EMAIL}</a>, call <a href="tel:{PHONE_TEL}">{PHONE}</a>, or <a href="/submit/">send us your manuscript</a>.</p>
    </div>
  </div>
</section>
'''
    return page('/about/', 'About', 'OmniMedia Syndicated Books is an Atlanta publishing house that signs authors free and publishes in paperback, ebook, and audiobook.', body)

def faq():
    items = ''.join(
        f'<details><summary>{e(f["q"])}<span class="pm" aria-hidden="true">+</span></summary><div class="answer">{f["a"]}</div></details>'
        for f in FAQ)
    body = f'''<section class="page-hero wrap">
  <p class="eyebrow">Questions, answered</p>
  <h1 class="display">FAQ</h1>
  <p class="lede">Can&rsquo;t find it here? Ask Chloe in the corner of your screen, or <a href="/submit/">send us a message</a>.</p>
</section>
<section class="section wrap"><div class="faq">{items}</div></section>
'''
    return page('/faq/', 'FAQ', 'Answers about publishing with OMS Books: free signing, the six-figure signing bonus, boutique services, formats, and film.', body)

def submit():
    body = f'''<section class="page-hero wrap">
  <p class="eyebrow">Start here</p>
  <h1 class="display">Submit</h1>
  <p class="lede">Tell us about you and your book. Our team reviews submissions within 24 to 48 hours.</p>
</section>
<section class="section wrap">
  <div class="cols">
    <div>
      <h2>What happens next</h2>
      <div class="prose" style="margin-top:20px">
        <p>We read every submission. If your book is a fit, we&rsquo;ll reach out to talk through the right path, whether that&rsquo;s signing, bonus consideration, or a boutique package.</p>
        <p class="fine">Please don&rsquo;t send full manuscripts yet. We&rsquo;ll ask for them.</p>
      </div>
    </div>
    <form class="form-card" name="submission" method="POST" action="/thank-you/?form=submission" data-netlify="true" netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="submission">
      <p class="hp"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
      <fieldset>
        <legend class="legend">What are you looking for?</legend>
        <div class="choices">
          <label class="choice"><input type="radio" name="path" value="signed" checked><span><strong>Get signed (free)</strong>Publish with OMS Books at no cost.</span></label>
          <label class="choice"><input type="radio" name="path" value="bonus"><span><strong>Signing bonus consideration</strong>I have multiple published books and a completed manuscript.</span></label>
          <label class="choice"><input type="radio" name="path" value="boutique"><span><strong>Boutique services</strong>I want to keep my rights and hire specific services.</span></label>
        </div>
      </fieldset>
      <div class="row2">
        <div class="field"><label for="f-name">Full name</label><input id="f-name" name="name" required autocomplete="name"></div>
        <div class="field"><label for="f-pen">Pen name (optional)</label><input id="f-pen" name="pen-name"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="f-email">Email</label><input id="f-email" type="email" name="email" required autocomplete="email"></div>
        <div class="field"><label for="f-phone">Phone</label><input id="f-phone" type="tel" name="phone" autocomplete="tel"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="f-title">Book title</label><input id="f-title" name="book-title"></div>
        <div class="field"><label for="f-genre">Genre</label><input id="f-genre" name="genre" placeholder="e.g. dark romance"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="f-status">Manuscript status</label>
          <select id="f-status" name="manuscript-status"><option>Complete</option><option>In progress</option><option>Just an idea</option></select></div>
        <div class="field"><label for="f-published">Books already published</label>
          <select id="f-published" name="books-published"><option>None yet</option><option>1</option><option>2 to 4</option><option>5 or more</option></select></div>
      </div>
      <fieldset>
        <legend class="legend">Boutique services you&rsquo;re interested in</legend>
        <div class="checks">
          <label><input type="checkbox" name="services" value="Editing"> Editing</label>
          <label><input type="checkbox" name="services" value="Ghostwriting"> Ghostwriting</label>
          <label><input type="checkbox" name="services" value="Cover design"> Cover design</label>
          <label><input type="checkbox" name="services" value="Formatting"> Formatting</label>
          <label><input type="checkbox" name="services" value="Audiobook"> Audiobook</label>
          <label><input type="checkbox" name="services" value="Marketing"> Marketing</label>
        </div>
      </fieldset>
      <div class="field"><label for="f-summary">Book summary</label><textarea id="f-summary" name="summary" required placeholder="A few paragraphs about your story and where it stands."></textarea></div>
      <div class="field"><label for="f-links">Links (optional)</label><input id="f-links" name="links" placeholder="Amazon author page, website, or socials"><span class="hint">Experienced authors: share your Amazon author page.</span></div>
      <label class="checks" style="display:flex;grid-template-columns:none;margin-bottom:24px"><input type="checkbox" name="join-mailing-list" value="yes"> <span style="font-family:var(--sans);font-size:16px">Add me to the OMS mailing list</span></label>
      <button class="btn btn-blue" type="submit" style="width:100%">Send submission {ARROW}</button>
      <p class="fine" style="margin-top:14px">By submitting, you confirm you own the rights to your work and agree to our <a href="/terms-and-conditions/">terms</a> and <a href="/privacy-policy/">privacy policy</a>.</p>
    </form>
  </div>
</section>
'''
    return page('/submit/', 'Submit Your Manuscript', 'Submit your book to OMS Books for free signing, six-figure signing bonus consideration, or boutique services.', body, news=False)

def thank_you():
    body = f'''<section class="page-hero wrap" style="border-bottom:0;padding-bottom:88px">
  <p class="eyebrow">Received</p>
  <h1 class="display">Thank you.</h1>
  <p class="lede" id="ty-msg">We&rsquo;ve got it. If you sent a submission, our team will review it within 24 to 48 hours.</p>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:32px"><a class="btn btn-ink" href="/books/">See our books {ARROW}</a><a class="btn" href="/">Back home {ARROW}</a></div>
</section>
<script>if(location.search.indexOf('form=newsletter')>-1){{document.getElementById('ty-msg').textContent='You\\u2019re on the list. Watch your inbox for cover reveals and release dates.';}}</script>
'''
    return page('/thank-you/', 'Thank You', 'Thanks for reaching out to OMS Books.', body, news=False)

LEGAL = {
    'privacy-policy': ('Privacy Policy', [
        ('', 'At OmniMedia Syndicated Books, we are committed to maintaining the trust and confidence of all visitors to our website. This Privacy Policy details how we handle the personal information and manuscript data you send to us.'),
        ('1. Information we collect', 'When you interact with our online forms, we collect personal contact information (such as full name, email address, and phone number) and manuscript documents, outlines, or synopses.'),
        ('2. How we use your data', 'We process your information to assess your publishing candidacy, evaluate potential signing bonuses, and communicate with you.'),
        ('3. Manuscript security and copyright', 'All submitted work is kept secure. We do not share your intellectual property with uncertified third parties.'),
    ]),
    'terms-and-conditions': ('Terms and Conditions', [
        ('', 'By accessing our website or submitting a publishing inquiry, you agree to comply with the standard terms of OmniMedia Syndicated Books.'),
        ('1. Submission validity', 'You declare that you hold full, undivided copyright ownership of any manuscript materials, outlines, or assets submitted through our website. Plagiarized or unoriginal drafts will be removed.'),
        ('2. Signing bonus terms', 'Any six-figure signing bonuses described on our website are selective and dependent on a publishing agreement signed by both parties after editorial review.'),
        ('3. Right to decline', 'OmniMedia Syndicated Books reserves the right to decline any submission that does not meet our professional standards.'),
    ]),
    'refund-policy': ('Refund Policy', [
        ('', 'Because our editorial, cover design, and marketing work is customized for each manuscript, we maintain the following refund criteria for paid services.'),
        ('1. Cancellations', 'You may request a full refund of any deposit within 24 hours of signing up for a paid service, provided our editors have not yet begun work on your manuscript.'),
        ('2. Work in progress', 'Once editing, design, or other work has begun, refunds will be calculated pro rata based on the labor hours already completed.'),
        ('3. After publication', 'Refunds cannot be issued after a title has been published and distributed to retailers.'),
    ]),
}

def legal(slug):
    title, parts = LEGAL[slug]
    content = ''.join((f'<h2>{e(h)}</h2>' if h else '') + f'<p>{e(t)}</p>' for h, t in parts)
    body = f'''<section class="page-hero wrap">
  <p class="eyebrow">Effective June 15, 2026</p>
  <h1 class="display" style="font-size:clamp(52px,8vw,110px)">{title}</h1>
</section>
<section class="section wrap"><div class="prose">{content}<p class="fine" style="margin-top:40px">Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div></section>
'''
    return page(f'/{slug}/', title, f'{title} for OmniMedia Syndicated Books.', body, news=False)

def not_found():
    body = f'''<section class="page-hero wrap" style="border-bottom:0;padding-bottom:88px">
  <p class="eyebrow">Error 404</p>
  <h1 class="display">Page not found</h1>
  <p class="lede">This page wandered off the shelf.</p>
  <div style="margin-top:32px"><a class="btn btn-ink" href="/">Back home {ARROW}</a></div>
</section>
'''
    return page('/404', 'Page Not Found', 'Page not found.', body, news=False)

# ---------------------------------------------------------------- write
def write(rel, text):
    p = os.path.join(DIST, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(text)

def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    shutil.copytree(os.path.join(ROOT, 'assets'), os.path.join(DIST, 'assets'))
    write('assets/js/faq-data.js', 'window.OMS_FAQ = ' + json.dumps(
        [dict(q=f['q'], a=f['a'], keys=f['keys'], chip=f['chip']) for f in FAQ], ensure_ascii=False, indent=1) + ';\n')
    write('index.html', home())
    write('books/index.html', books())
    write('get-signed/index.html', get_signed())
    write('boutique/index.html', boutique())
    write('page-to-screen/index.html', page_to_screen())
    write('about/index.html', about())
    write('faq/index.html', faq())
    write('submit/index.html', submit())
    write('thank-you/index.html', thank_you())
    for slug in LEGAL:
        write(f'{slug}/index.html', legal(slug))
    write('404.html', not_found())
    write('_redirects', '\n'.join([
        '/services            /boutique/        301',
        '/services/           /boutique/        301',
        '/marketing-and-promotion   /page-to-screen/   301',
        '/marketing-and-promotion/  /page-to-screen/   301',
        '/publications        /books/           301',
        '/publications/       /books/           301',
    ]) + '\n')
    write('netlify.toml', '[build]\n  publish = "."\n\n[[headers]]\n  for = "/assets/*"\n  [headers.values]\n    Cache-Control = "public, max-age=604800"\n')
    write('robots.txt', 'User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % SITE)
    urls = ['/', '/books/', '/get-signed/', '/boutique/', '/page-to-screen/', '/about/', '/faq/', '/submit/'] + [f'/{s}/' for s in LEGAL]
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          ''.join(f'  <url><loc>{SITE}{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    print('built', DIST)

if __name__ == '__main__':
    main()
