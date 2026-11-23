"""Erencan Elektrik sitesini üretir (Türkçe + İngilizce).

Kullanım (repo kökünden):  python3 _build/build_site.py
Türkçe sayfalar kökte, İngilizce sayfalar /en/ altında yazılır. Hizmet metinleri
pages_data.py (TR) ve pages_data_en.py (EN), logo listeleri logo_lists.json,
Türkçe ana sayfanın <head> kısmı ve işletme şeması head_home.html içindedir.
sitemap.xml de buradan üretilir. _build klasörü GitHub Pages'te yayınlanmaz.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
V = "15"  # önbellek sürümü: CSS/JS/görsel değişince artırın
TODAY = "2026-11-24"

from pages_data import PAGES  # noqa: E402
from pages_data_en import PAGES_EN  # noqa: E402

SITE = "https://erencanelektrik.com"
TEL = "+905325861860"
TEL_TXT = "0532 586 18 60"
TEL_INTL = "+90 532 586 18 60"
WA = "https://wa.me/905325861860"
MAIL = "erencanelektrik@gmail.com"
ADDR_LINE1 = "Beylikdüzü OSB Mah., Birlik Sanayi Sitesi"
ADDR_LINE2 = "2. Cad. No:1/1 D:4, 34524 Beylikdüzü / İstanbul"
MAPS = "https://maps.app.goo.gl/eDhi7KrXCUre3yDB6"
REVIEW = "https://g.page/r/CSnbCvFlFnZ-EBM/review"
MAP_EMBED = ("https://maps.google.com/maps?q=Erencan+Elektrik,+Birlik+Sanayi+Sitesi,"
             "+Beylikd%C3%BCz%C3%BC,+%C4%B0stanbul&z=16&output=embed")
# Web3Forms erişim anahtarı (herkese açık olması sorun değil); talepler MAIL adresine düşer
FORM_KEY = "0bd47888-8667-4523-94ac-44d884d8b230"
TRADE = "Erencan Elektrik İnşaat Taahhüt San. ve Tic. Ltd. Şti."

LOGOS = json.load(open(os.path.join(HERE, "logos.json"), encoding="utf-8"))
BY_STEM = {os.path.splitext(os.path.basename(v["file"]))[0]: v for v in LOGOS.values()}
LISTS = json.load(open(os.path.join(HERE, "logo_lists.json"), encoding="utf-8"))

FONT = ('<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/saira-latin-wdth-normal.woff2" crossorigin>\n'
        '  <link rel="preload" as="font" type="font/woff2" href="/assets/fonts/saira-latin-ext-wdth-normal.woff2" crossorigin>\n'
        '  <script>document.documentElement.classList.add("js")</script>')

# ---------- sayfa eşleşmeleri (dil geçişi ve hreflang için) ----------
EN_OF = {"/": "/en/", "/teklif-al/": "/en/quote/", "/teklif-al/tesekkurler/": "/en/quote/thank-you/",
         "/kvkk/": "/en/privacy/"}
for _e in PAGES_EN:
    EN_OF[f"/{_e['tr']}/"] = f"/{_e['slug']}/"
TR_OF = {v: k for k, v in EN_OF.items()}
EN_BY_TR = {e["tr"]: e for e in PAGES_EN}


def alt_of(path):
    return EN_OF.get(path) or TR_OF.get(path)


def lang_of(path):
    return "en" if path.startswith("/en/") else "tr"


# ---------- arayüz metinleri ----------
T = {
    "tr": {
        "home": "/", "quote": "/teklif-al/", "privacy": "/kvkk/",
        "nav": [("Hizmetler", "#hizmetler"), ("Markalar", "#markalar"), ("Referanslar", "#referanslar"),
                ("Hakkımızda", "#hakkimizda"), ("SSS", "#sss"), ("İletişim", "#iletisim")],
        "nav_quote": "Teklif al", "skip": "İçeriğe geç", "home_label": "Erencan Elektrik ana sayfa",
        "menu": "Menü", "close": "Kapat", "main_menu": "Ana menü", "call": "Bizi arayın", "lang_label": "Dil",
        "call_short": "Ara", "quick": "Hızlı iletişim", "wa": "WhatsApp'tan yazın", "ask_quote": "Teklif isteyin",
        "hours": "Pazartesi–Cumartesi 08:00–19:00",
        "facts": [("Kuruluş", "2004, Beylikdüzü"), ("Satış", "Perakende ve toptan"),
                  ("Gönderim", "Türkiye'nin her yerine"), ("Açık", "Pzt–Cmt 08:00–19:00")],
        "facts_label": "Firma bilgileri",
        "f_services": "Hizmetler", "f_hours": "Çalışma saatleri", "f_review": "Google'da değerlendirin",
        "f_privacy": "KVKK aydınlatma metni",
        "crumb_home": "Ana sayfa", "crumb_label": "Sayfa konumu", "ld_home": "Ana Sayfa",
        "more": "Hizmeti inceleyin", "faq_h": "Sıkça sorulan sorular", "others": "Diğer hizmetlerimiz",
        "others_label": "Diğer hizmetler",
        "faq_note": 'Aradığınızı bulamadıysanız <a href="/teklif-al/">teklif formundan</a> yazın ya da <a href="tel:{TEL}">arayın</a>.',
        "c_addr": "Adres", "c_tel": "Telefon ve WhatsApp", "c_mail": "E-posta", "c_hours": "Çalışma saatleri",
        "c_area": "Hizmet bölgesi", "c_area_v": "Beylikdüzü merkezli, İstanbul geneli. Malzeme gönderimi Türkiye geneline.",
        "c_map": "Google Haritalar'da aç", "c_h": "İletişim", "map_title": "Erencan Elektrik konumu",
        "review": 'Bizimle çalıştıysanız <a href="{REVIEW}" rel="noopener">Google\'da değerlendirmenizi</a> bekleriz.',
        "store_alt": "Erencan Elektrik'in Birlik Sanayi Sitesi'ndeki mağazası",
    },
    "en": {
        "home": "/en/", "quote": "/en/quote/", "privacy": "/en/privacy/",
        "nav": [("Services", "#services"), ("Brands", "#brands"), ("Clients", "#clients"),
                ("About", "#about"), ("FAQ", "#faq"), ("Contact", "#contact")],
        "nav_quote": "Get a quote", "skip": "Skip to content", "home_label": "Erencan Elektrik home page",
        "menu": "Menu", "close": "Close", "main_menu": "Main menu", "call": "Call us", "lang_label": "Language",
        "call_short": "Call", "quick": "Quick contact", "wa": "Message on WhatsApp", "ask_quote": "Request a quote",
        "hours": "Monday–Saturday 08:00–19:00",
        "facts": [("Founded", "2004, Beylikdüzü"), ("Sales", "Retail and wholesale"),
                  ("Shipping", "Anywhere in Türkiye"), ("Open", "Mon–Sat 08:00–19:00")],
        "facts_label": "Company facts",
        "f_services": "Services", "f_hours": "Opening hours", "f_review": "Review us on Google",
        "f_privacy": "Privacy notice",
        "crumb_home": "Home", "crumb_label": "Breadcrumb", "ld_home": "Home",
        "more": "View service", "faq_h": "Frequently asked questions", "others": "Other services",
        "others_label": "Other services",
        "faq_note": 'Can\'t find what you need? Use the <a href="/en/quote/">quote form</a> or <a href="tel:{TEL}">call us</a>.',
        "c_addr": "Address", "c_tel": "Phone and WhatsApp", "c_mail": "Email", "c_hours": "Opening hours",
        "c_area": "Service area", "c_area_v": "Based in Beylikdüzü, serving all of Istanbul. Materials shipped across Türkiye.",
        "c_map": "Open in Google Maps", "c_h": "Contact", "map_title": "Erencan Elektrik location",
        "review": 'If you have worked with us, we would appreciate a <a href="{REVIEW}" rel="noopener">review on Google</a>.',
        "store_alt": "Erencan Elektrik's shop in Birlik Sanayi Sitesi, Beylikdüzü",
    },
}
for _l in T.values():
    for _k in ("faq_note", "review"):
        _l[_k] = _l[_k].replace("{TEL}", TEL).replace("{REVIEW}", REVIEW)

ICONS = {
    "elektrik-malzemesi": '<rect x="14" y="6" width="20" height="36" rx="2"/><path d="M14 14h20M14 34h20"/><rect x="20" y="19" width="8" height="10" rx="1"/><path d="M24 19v-3"/>',
    "pano-tasarim-montaj": '<rect x="9" y="5" width="30" height="38" rx="2"/><path d="M24 5v38"/><path d="M14 13h5M14 19h5M29 13h5M29 19h5"/><circle cx="21" cy="28" r="1.2"/><circle cx="27" cy="28" r="1.2"/>',
    "elektrik-taahhut": '<path d="M7 43V17l12-8 12 8v26"/><path d="M3 43h42"/><path d="M31 25h10v18"/><path d="M20 20l-4 9h6l-3 8"/>',
    "proje-muhendislik": '<path d="M9 7h22l8 8v26H9z"/><path d="M31 7v8h8"/><path d="M15 23h18M15 29h18M15 35h10"/>',
}


def icon(slug, size=48):
    return (f'<svg class="ico" viewBox="0 0 48 48" width="{size}" height="{size}" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[slug]}</svg>')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def ld_tags(lds):
    return "\n".join('  <script type="application/ld+json">\n' + json.dumps(x, ensure_ascii=False, indent=2)
                     + "\n  </script>" for x in lds)


def logo(stem_or_key, alt, size=1.0):
    v = LOGOS.get(stem_or_key) or BY_STEM[os.path.splitext(stem_or_key)[0]]
    w, h = round(v["w"] * size), round(v["h"] * size)
    return (f'<img src="/{v["file"]}?v={V}" width="{w}" height="{h}" alt="{alt}" '
            f'loading="lazy" decoding="async">')


def marquee(items, label, speed=38, size=1.0):
    """Kayan logo şeridi. İkinci kopya yalnızca döngü için, ekran okuyuculardan gizli."""
    one = "".join(f"<li>{logo(f, alt, size).replace(' loading=\"lazy\"', '')}</li>" for alt, f in items)
    two = "".join(f"<li>{logo(f, '', size).replace(' loading=\"lazy\"', '')}</li>" for alt, f in items)
    dur = round(len(items) * 180 / speed)
    return (f'<div class="marquee" style="--dur:{dur}s">'
            f'<ul class="marquee-track" aria-label="{label}">{one}</ul>'
            f'<ul class="marquee-track" aria-hidden="true">{two}</ul></div>')


# ---------- ortak <head> ----------
def head(lang, title, desc, path, lds=(), noindex=False, preload_hero=False):
    url = f"{SITE}{path}"
    alt = alt_of(path)
    robots = '\n  <meta name="robots" content="noindex">' if noindex else ""
    tr_path, en_path = (path, alt) if lang == "tr" else (alt, path)
    hreflang = (f'\n  <link rel="alternate" hreflang="tr" href="{SITE}{tr_path}">'
                f'\n  <link rel="alternate" hreflang="en" href="{SITE}{en_path}">'
                f'\n  <link rel="alternate" hreflang="x-default" href="{SITE}{tr_path}">') if alt and not noindex else ""
    loc, loc_alt = ("tr_TR", "en_US") if lang == "tr" else ("en_US", "tr_TR")
    pre = (f'\n  <link rel="preload" as="image" href="/assets/vitrin.webp?v={V}" fetchpriority="high" media="(min-width: 901px)">'
           f'\n  <link rel="preload" as="image" href="/assets/vitrin-900.webp?v={V}" fetchpriority="high" media="(max-width: 900px)">') if preload_hero else ""
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{esc(title)}</title>{pre}
  <meta name="description" content="{esc(desc)}">{robots}
  <link rel="canonical" href="{url}">{hreflang}
  <meta name="theme-color" content="#093b6f">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{loc}">
  <meta property="og:locale:alternate" content="{loc_alt}">
  <meta property="og:site_name" content="Erencan Elektrik">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/hakkimizda1.jpg">
  <meta name="twitter:card" content="summary_large_image">
  {FONT}
  <link rel="stylesheet" href="/style.css?v={V}">
  <link rel="icon" type="image/x-icon" href="/assets/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32x32.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
{ld_tags(lds)}
</head>
'''


def breadcrumb_ld(lang, name, path):
    t = T[lang]
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": t["ld_home"], "item": f"{SITE}{t['home']}"},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"{SITE}{path}"}]}


def crumbs(lang, name):
    t = T[lang]
    return (f'<nav class="crumbs" aria-label="{t["crumb_label"]}"><a href="{t["home"]}">{t["crumb_home"]}</a>'
            f'<span aria-hidden="true">/</span><span aria-current="page">{name}</span></nav>')


# ---------- üst menü, alt bilgi ----------
def header(lang, path):
    t = T[lang]
    base = "" if path == t["home"] else t["home"]
    links = "".join(f'<li><a href="{base}{href}">{name}</a></li>' for name, href in t["nav"])
    q = t["quote"]
    links += f'<li><a href="{q}"{" aria-current=\"page\"" if path.startswith(q) else ""}>{t["nav_quote"]}</a></li>'
    alt = alt_of(path) or ("/en/" if lang == "tr" else "/")
    tr_href, en_href = (path, alt) if lang == "tr" else (alt, path)
    sw = (f'<div class="lang-switch" role="group" aria-label="{t["lang_label"]}">'
          f'<a href="{tr_href}" lang="tr" hreflang="tr"{" aria-current=\"true\"" if lang == "tr" else ""}>TR</a>'
          f'<a href="{en_href}" lang="en" hreflang="en"{" aria-current=\"true\"" if lang == "en" else ""}>EN</a></div>')
    return f'''<a class="skip" href="#icerik">{t["skip"]}</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="{t["home"]}" aria-label="{t["home_label"]}">
      <img src="/assets/logo.webp?v={V}" alt="" width="60" height="60">
      <span class="brand-name"><span>Erencan</span><span>Elektrik</span></span>
    </a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-menu" data-open="{t["menu"]}" data-close="{t["close"]}">{t["menu"]}</button>
    <nav aria-label="{t["main_menu"]}">
      <ul class="menu" id="site-menu">{links}</ul>
    </nav>
    <a class="bar-tel" href="tel:{TEL}" aria-label="{t["call"]}: {TEL_TXT}">{t["call"]}</a>
    {sw}
  </div>
</header>'''


def services_of(lang):
    """(tr_slug, path, nav, h1) listesi"""
    if lang == "tr":
        return [(p["slug"], f'/{p["slug"]}/', p["nav"]) for p in PAGES]
    return [(e["tr"], f'/{e["slug"]}/', e["nav"]) for e in PAGES_EN]


def footer(lang):
    t = T[lang]
    services = "".join(f'<li><a href="{path}">{nav}</a></li>' for _, path, nav in services_of(lang))
    return f'''<footer class="site-footer">
  <div class="wrap foot">
    <div>
      <p class="foot-name">{TRADE}</p>
      <p>{ADDR_LINE1}<br>{ADDR_LINE2}</p>
      <p><a href="tel:{TEL}">{TEL_TXT if lang == "tr" else TEL_INTL}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p>
    </div>
    <div>
      <p class="foot-h">{t["f_services"]}</p>
      <ul>{services}</ul>
    </div>
    <div>
      <p class="foot-h">{t["f_hours"]}</p>
      <p>{t["hours"]}</p>
      <p><a href="https://instagram.com/erencanelektrik" rel="noopener">Instagram</a><br><a href="{REVIEW}" rel="noopener">{t["f_review"]}</a><br><a href="{t["privacy"]}">{t["f_privacy"]}</a></p>
    </div>
  </div>
  <p class="wrap copy">© 2026 Erencan Elektrik</p>
</footer>
<div class="quickbar" aria-label="{t["quick"]}">
  <a href="tel:{TEL}">{t["call_short"]}</a>
  <a href="{WA}" rel="noopener">WhatsApp</a>
</div>
<script src="/app.js?v={V}" defer></script>'''


def plate(lang):
    t = T[lang]
    cells = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in t["facts"])
    return f'<dl class="facts" aria-label="{t["facts_label"]}">{cells}</dl>'


def faq(items):
    return "\n".join(f'''      <details>
        <summary>{q}</summary>
        <p>{a}</p>
      </details>''' for q, a in items)


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
        for q, a in items]}


def actions(lang, konu=None, call=True):
    t = T[lang]
    q = f"?konu={konu}" if konu else ""
    tel = (f'\n        <a class="btn btn-line" href="tel:{TEL}" aria-label="{t["call"]}: {TEL_TXT}">{t["call"]}</a>'
           if call else "")
    return f'''<div class="actions">
        <a class="btn" href="{t["quote"]}{q}">{t["ask_quote"]}</a>
        <a class="btn btn-line" href="{WA}" rel="noopener">{t["wa"]}</a>{tel}
      </div>'''


def cta(lang, title, text, konu=None):
    t = T[lang]
    q = f"?konu={konu}" if konu else ""
    return f'''  <section class="cta-band">
    <div class="wrap cta-inner">
      <div>
        <h2>{title}</h2>
        <p>{text}</p>
      </div>
      <div class="cta-actions">
        <a class="btn btn-light" href="{t["quote"]}{q}">{t["ask_quote"]}</a>
        <a class="btn btn-ghost" href="{WA}" rel="noopener">{t["wa"]}</a>
      </div>
    </div>
  </section>'''


def contact_block(lang, sid):
    t = T[lang]
    return f'''  <section class="block block-steel" id="{sid}">
    <div class="wrap contact">
      <div>
        <h2>{t["c_h"]}</h2>
        <dl class="contact-list">
          <div><dt>{t["c_addr"]}</dt><dd><address>{ADDR_LINE1}<br>{ADDR_LINE2}</address><a href="{MAPS}" rel="noopener">{t["c_map"]}</a></dd></div>
          <div><dt>{t["c_tel"]}</dt><dd><a href="tel:{TEL}">{TEL_TXT if lang == "tr" else TEL_INTL}</a></dd></div>
          <div><dt>{t["c_mail"]}</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
          <div><dt>{t["c_hours"]}</dt><dd>{t["hours"]}</dd></div>
          <div><dt>{t["c_area"]}</dt><dd>{t["c_area_v"]}</dd></div>
        </dl>
        {actions(lang)}
        <p class="review-note">{t["review"]}</p>
      </div>
      <iframe class="map" title="{t["map_title"]}" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
  </section>'''


# ---------- ana sayfa içerikleri ----------
HOME = {
    "tr": {
        "title": "Erencan Elektrik | Beylikdüzü Elektrik Malzemesi ve Pano",
        "desc": "2004'ten beri Beylikdüzü'nde perakende ve toptan elektrik malzemesi, pano imalatı ve elektrik taahhüdü. Siemens, Schneider, Viko stokta; Türkiye'ye gönderim.",
        "kicker": "Birlik Sanayi Sitesi, Beylikdüzü",
        "h1": "Beylikdüzü'nde elektrik malzemesi, pano ve taahhüt",
        "lead": "2004'ten beri şalt, kablo ve pano malzemesi satıyor; fabrika, ticari yapı ve konut projelerinin elektrik işlerini üstleniyoruz.",
        "services_h": "Hizmetlerimiz",
        "services": {
            "elektrik-malzemesi": ("Elektrik malzemesi satışı", "Şalt, kablo, bağlantı ve pano malzemeleri stokta. Tek parça da satıyoruz, firmalara toptan fiyat ve cari hesap açıyoruz."),
            "pano-tasarim-montaj": ("Pano tasarımı ve montajı", "IEC standartlarında endüstriyel ve bina tipi panolar. Teklifi onayladığınızda imalata başlıyoruz."),
            "elektrik-taahhut": ("Elektrik taahhüdü", "Fabrika, ticari yapı ve konut projelerinde alçak gerilim, bina içi tesisat ve dış saha uygulamaları. Keşif ücretsiz."),
            "proje-muhendislik": ("Proje ve mühendislik", "Yük hesapları, projelendirme ve teknik şartname uyumu. Projeyi hazırlayan ekip sahada da uyguluyor."),
        },
        "band": "Şalt, kablo ve pano malzemesi raflarımızda. Tek sigortadan proje siparişine kadar.",
        "figures": [("2004", "yılından beri Beylikdüzü'nde"), ("{n}", "markanın ürünleri stokta"), ("Türkiye", "geneline malzeme gönderimi")],
        "brands_h": "Satışını yaptığımız markalar", "brands_note": "Bu markaların ürünleri mağazamızda stokta.",
        "refs_h": "Çalıştığımız firmalardan bazıları", "brands_label": "Satışını yaptığımız markalar", "refs_label": "Referans firmalar",
        "about_h": "Hakkımızda",
        "about": ["Erencan Elektrik 2004 yılında Beylikdüzü'nde kuruldu. Endüstriyel elektrik sistemleri ve projelendirme alanında çalışan kadromuzla Türkiye'nin birçok bölgesinde bireysel ve kurumsal müşterilere hizmet verdik.",
                  "Alçak gerilim sistemleri, pano kurulumu, bina içi tesisat ve dış saha uygulamalarını standartlara uygun malzemeyle yapıyoruz. Malzemeyi kendi stoğumuzdan sağladığımız için projeyi baştan sona tek elden yürütebiliyoruz."],
        "alt_cables": "Stoktaki kablo makaraları ve pano malzemeleri", "alt_front": "Erencan Elektrik mağaza cephesi",
        "cta_h": "Malzeme listenizi gönderin, fiyatını çıkaralım",
        "cta_p": "Ürün, marka ve adetleri yazmanız yeterli. Firmalara toptan fiyat ve cari hesap açıyoruz.",
        "ids": ("hizmetler", "markalar", "referanslar", "hakkimizda", "sss", "iletisim"),
        "faq": [
            ("Tek parça (perakende) malzeme alabilir miyim?", "Evet. Mağazamızda hem perakende hem toptan satış yapıyoruz; tek bir sigortadan büyük proje siparişlerine kadar malzeme temin edebilirsiniz."),
            ("Toptan alan firmalara özel fiyat veya cari hesap imkânı var mı?", "Evet. Düzenli ve toptan alım yapan firmalara özel fiyat ve cari hesap imkânı sunuyoruz. Detaylar için bizimle iletişime geçebilirsiniz."),
            ("Hangi markaların ürünlerini satıyorsunuz?", "Siemens, Schneider Electric, Legrand, Viko, Entes, Emas, Omron, Finder, Philips, Nexans ve Öznur başta olmak üzere sektörün önde gelen markalarının şalt, kablo, aydınlatma ve pano malzemelerini satıyoruz."),
            ("Malzeme teslimatı veya kargo yapıyor musunuz?", "Evet. Türkiye'nin her yerine malzeme gönderimi yapıyoruz."),
            ("Pano siparişinde süreç nasıl işliyor?", "İhtiyacınıza göre teklif hazırlıyoruz; teklif onaylandıktan sonra panonun imalatına başlıyoruz. Teslim süresi panonun tipine ve büyüklüğüne göre değişir; net süreyi teklif aşamasında bildiriyoruz."),
            ("Elektrik taahhüt işlerinde keşif ücretli mi?", "Hayır, keşif ücretsizdir."),
            ("Hangi bölgelere hizmet veriyorsunuz?", "Beylikdüzü merkezli olarak İstanbul genelinde hizmet veriyoruz. İstanbul dışındaki projelere de iş ve malzeme gönderimi yapıyoruz."),
            ("Ödeme seçenekleri nelerdir?", "Nakit, kredi kartı ve havale/EFT ile ödeme kabul ediyoruz."),
            ("Ürünlerde garanti nasıl işliyor?", "Sattığımız tüm ürünlerde üretici firmanın garanti koşulları geçerlidir."),
            ("Çalışma saatleriniz nedir, nasıl teklif alabilirim?", "Pazartesi–Cumartesi 08:00–19:00 arası açığız. Teklif için sitemizdeki teklif formunu doldurabilir, 0532 586 18 60 numarasından arayabilir veya WhatsApp'tan yazabilirsiniz."),
        ],
    },
    "en": {
        "title": "Erencan Elektrik | Electrical Supplies & Panels, Istanbul",
        "desc": "Retail and wholesale electrical supplies, panel building and electrical contracting in Beylikdüzü, Istanbul since 2004. Shipping across Türkiye.",
        "kicker": "Birlik Sanayi Sitesi, Beylikdüzü, Istanbul",
        "h1": "Electrical supplies, panels and contracting in Istanbul",
        "lead": "Since 2004 we have been selling switchgear, cables and panel components from our shop in Beylikdüzü, and carrying out electrical work for factories, commercial buildings and housing projects.",
        "services_h": "Our services",
        "services": {
            "elektrik-malzemesi": ("Electrical supplies", "Switchgear, cables, wiring accessories and panel components in stock. Single items for anyone; wholesale pricing and trade accounts for companies."),
            "pano-tasarim-montaj": ("Panel design and installation", "IEC-compliant industrial and building distribution panels. Manufacture starts once you approve the quotation."),
            "elektrik-taahhut": ("Electrical contracting", "Low-voltage systems, interior wiring and site work for factories, commercial buildings and housing. Free site survey."),
            "proje-muhendislik": ("Engineering and design", "Load calculations, project design and specification compliance. The team that designs the project also installs it."),
        },
        "band": "Switchgear, cables and panel components on our shelves, from a single breaker to a full project order.",
        "figures": [("2004", "founded in Beylikdüzü"), ("{n}", "brands in stock"), ("Türkiye", "nationwide shipping")],
        "brands_h": "Brands we sell", "brands_note": "Products from these brands are in stock at our shop.",
        "refs_h": "Some of the companies we work with", "brands_label": "Brands we sell", "refs_label": "Client companies",
        "about_h": "About us",
        "about": ["Erencan Elektrik was founded in Beylikdüzü, Istanbul, in 2004. With a team experienced in industrial electrical systems and project design, we have served private and corporate customers in many regions of Türkiye.",
                  "We install low-voltage systems, panels, interior wiring and outdoor electrical works using standard-compliant materials. Because the materials come from our own stock, we can run a project from start to finish as a single contractor."],
        "alt_cables": "Cable reels and panel components in stock", "alt_front": "Erencan Elektrik shop front",
        "cta_h": "Send us your material list for a price",
        "cta_p": "Just list the products, brands and quantities. Companies get wholesale pricing and trade accounts.",
        "ids": ("services", "brands", "clients", "about", "faq", "contact"),
        "faq": [
            ("Can I buy a single item?", "Yes. Our shop sells both retail and wholesale, from a single circuit breaker to large project orders."),
            ("Do you offer trade pricing or accounts for companies?", "Yes. Companies that order regularly or in bulk get special pricing and can open a trade account. Contact us for details."),
            ("Which brands do you sell?", "We sell switchgear, cables, lighting and panel components from leading brands including Siemens, Schneider Electric, Legrand, Viko, Entes, Emas, Omron, Finder, Philips, Nexans and Öznur."),
            ("Do you deliver or ship orders?", "Yes. We ship materials anywhere in Türkiye."),
            ("How does a panel order work?", "We prepare a quotation for your requirement and start manufacturing once it is approved. Lead time depends on the panel type and size; we confirm it with the quotation."),
            ("Is the site survey for contracting work free?", "Yes, the site survey is free of charge."),
            ("Which areas do you serve?", "We are based in Beylikdüzü and work across Istanbul. We also take on projects and ship materials outside Istanbul."),
            ("Which payment methods do you accept?", "Cash, credit card and bank transfer."),
            ("How does the warranty work?", "All products we sell carry the manufacturer's warranty."),
            ("What are your opening hours and how can I get a quote?", "We are open Monday to Saturday, 08:00–19:00. For a quote, use the quote form on this site, call +90 532 586 18 60 or message us on WhatsApp. We can reply in English by email."),
        ],
    },
}
SERVICE_ORDER = ["elektrik-malzemesi", "pano-tasarim-montaj", "elektrik-taahhut", "proje-muhendislik"]


def service_path(lang, tr_slug):
    return f"/{tr_slug}/" if lang == "tr" else f"/{EN_BY_TR[tr_slug]['slug']}/"


def business_ld_tr():
    h = open(os.path.join(HERE, "head_home.html"), encoding="utf-8").read()
    for b in re.findall(r'ld\+json">(.*?)</script>', h, re.S):
        d = json.loads(b)
        if d.get("@id", "").endswith("#isletme"):
            return d
    raise SystemExit("head_home.html içinde işletme şeması bulunamadı")


def business_ld(lang):
    d = business_ld_tr()
    d["contactPoint"] = {"@type": "ContactPoint", "contactType": "sales", "telephone": TEL_INTL, "email": MAIL,
                         "availableLanguage": ["Turkish", "English"], "url": f"{SITE}{T[lang]['quote']}"}
    if lang == "tr":
        return d
    d["url"] = f"{SITE}/"
    d["description"] = ("Electrical supplies (retail and wholesale), electrical panel design and installation, "
                        "electrical contracting and engineering in Beylikdüzü, Istanbul.")
    d["knowsAbout"] = ["Electrical contracting", "Electrical panel design and installation", "Low-voltage systems",
                       "Electrical supplies", "Electrical project design"]
    d["areaServed"] = [{"@type": "City", "name": "Istanbul"}, {"@type": "Country", "name": "Türkiye"}]
    d["paymentAccepted"] = "Cash, Credit Card, Bank Transfer"
    d["hasOfferCatalog"] = {"@type": "OfferCatalog", "name": "Electrical supplies", "itemListElement": [
        {"@type": "OfferCatalog", "name": "Switchgear", "description": "Circuit breakers, RCDs, contactors, thermal relays"},
        {"@type": "OfferCatalog", "name": "Cables", "description": "Power and control cables"},
        {"@type": "OfferCatalog", "name": "Switches, sockets and connectors"},
        {"@type": "OfferCatalog", "name": "Panels and panel components"},
        {"@type": "OfferCatalog", "name": "Relays and automation products"},
        {"@type": "OfferCatalog", "name": "Lighting"},
        {"@type": "OfferCatalog", "name": "Measuring instruments"}]}
    return d


def home(lang):
    t, h = T[lang], HOME[lang]
    path = t["home"]
    sid = dict(zip(("services", "brands", "clients", "about", "faq", "contact"), h["ids"]))
    cards = "\n".join(f'''        <li>
          <a href="{service_path(lang, s)}">
            {icon(s)}
            <h3>{h["services"][s][0]}</h3>
            <p>{h["services"][s][1]}</p>
            <span class="more">{t["more"]}</span>
          </a>
        </li>''' for s in SERVICE_ORDER)
    figs = "".join(f"<li><strong>{a.replace('{n}', str(len(LISTS['markalar'])))}</strong><span>{b}</span></li>"
                   for a, b in h["figures"])
    about = "".join(f"<p>{x}</p>" for x in h["about"])
    lds = [business_ld(lang), faq_ld(h["faq"]),
           {"@context": "https://schema.org", "@type": "WebSite", "name": "Erencan Elektrik", "url": f"{SITE}{path}",
            "inLanguage": lang, "publisher": {"@id": f"{SITE}/#isletme"}}]
    body = f'''<body>
{header(lang, path)}
<main id="icerik">
  <section class="hero1">
    <picture class="hero1-photo">
      <source media="(max-width: 900px)" srcset="/assets/vitrin-900.webp?v={V}">
      <img src="/assets/vitrin.webp?v={V}" width="1536" height="1044" alt="{t["store_alt"]}" fetchpriority="high">
    </picture>
    <div class="wrap hero1-inner">
      <p class="hero1-kicker">{h["kicker"]}</p>
      <h1 class="type-h1">{h["h1"]}</h1>
      <p class="lead">{h["lead"]}</p>
      <div class="actions">
        <a class="btn btn-light" href="{t["quote"]}">{t["ask_quote"]}</a>
        <a class="btn btn-ghost" href="{WA}" rel="noopener">{t["wa"]}</a>
      </div>
    </div>
  </section>
  <div class="facts-wrap">
    <div class="wrap">{plate(lang)}</div>
  </div>

  <section class="block" id="{sid["services"]}">
    <div class="wrap">
      <h2>{h["services_h"]}</h2>
      <ul class="cards">
{cards}
      </ul>
    </div>
  </section>

  <section class="photo-band">
    <img src="/assets/hakkimizda2.webp?v={V}" width="900" height="1200" alt="" loading="lazy" decoding="async">
    <div class="wrap photo-band-inner">
      <p class="big">{h["band"]}</p>
      <ul class="figures">{figs}</ul>
    </div>
  </section>

  <section class="block" id="{sid["brands"]}">
    <div class="wrap">
      <h2>{h["brands_h"]}</h2>
      <p class="section-note">{h["brands_note"]}</p>
      {marquee(LISTS["markalar"], h["brands_label"])}
    </div>
  </section>

  <section class="block block-steel" id="{sid["clients"]}">
    <div class="wrap">
      <h2>{h["refs_h"]}</h2>
      {marquee(LISTS["referanslar"], h["refs_label"], speed=32, size=.9)}
    </div>
  </section>

  <section class="block about-block" id="{sid["about"]}">
    <div class="wrap about1">
      <div class="about1-photos">
        <img src="/assets/hakkimizda3.webp?v={V}" width="900" height="1200" alt="{h["alt_cables"]}" loading="lazy" decoding="async">
        <img src="/assets/hakkimizda1.webp?v={V}" width="900" height="1200" alt="{h["alt_front"]}" loading="lazy" decoding="async">
      </div>
      <div class="about-text">
        <h2>{h["about_h"]}</h2>
        {about}
      </div>
    </div>
  </section>

{cta(lang, h["cta_h"], h["cta_p"])}

  <section class="block" id="{sid["faq"]}">
    <div class="wrap faq-grid">
      <div class="faq-head">
        <h2>{t["faq_h"]}</h2>
        <p>{t["faq_note"]}</p>
      </div>
      <div class="faq">
{faq(h["faq"])}
      </div>
    </div>
  </section>

{contact_block(lang, sid["contact"])}
</main>
{footer(lang)}
</body>
</html>
'''
    if lang == "tr":
        # Türkçe ana sayfa <head>'i head_home.html'den: işletme şeması orada elle tutuluyor
        hd = head(lang, h["title"], h["desc"], path, lds[1:], preload_hero=True)
        hd = hd.replace("</head>", ld_tags([lds[0]]) + "\n</head>")
        return hd + body
    return head(lang, h["title"], h["desc"], path, lds, preload_hero=True) + body


# ---------- hizmet sayfaları ----------
def block(title, kind, data):
    if kind == "list":
        inner = '<ul class="ticks">' + "".join(f"<li>{x}</li>" for x in data) + "</ul>"
    elif kind == "steps":
        inner = '<ol class="steps">' + "".join(f"<li><strong>{t}</strong><span>{d}</span></li>" for t, d in data) + "</ol>"
    elif kind == "brands":
        inner = '<ul class="logo-grid">' + "".join(f"<li>{logo(f, n)}</li>" for n, f in data) + "</ul>"
    else:
        inner = f"<p>{data}</p>"
    return f'''    <section class="sub-block">
      <h2>{title}</h2>
      {inner}
    </section>'''


SERVICE_CTA = {
    "tr": ("Bu hizmet için teklif alın", "Talebinizi formdan iletin, inceleyip size dönelim. Pazartesi–Cumartesi 08:00–19:00 arası arayabilir ya da WhatsApp'tan yazabilirsiniz."),
    "en": ("Get a quote for this service", "Send your request through the form and we will get back to you. You can also call us Monday–Saturday 08:00–19:00 or message us on WhatsApp."),
}


def service_page(lang, p):
    t = T[lang]
    tr_slug = p.get("tr", p["slug"])
    path = f"/{p['slug']}/"
    url = f"{SITE}{path}"
    siblings = PAGES if lang == "tr" else PAGES_EN
    others = "".join(f'<li><a href="/{o["slug"]}/">{icon(o.get("tr", o["slug"]), 28)}<span>{o["nav"]}</span></a></li>'
                     for o in siblings if o is not p)
    lds = [
        {"@context": "https://schema.org", "@type": "Service", "name": p["h1"], "serviceType": p["service_type"],
         "description": p["desc"], "url": url, "inLanguage": lang,
         "provider": {"@id": f"{SITE}/#isletme", "@type": ["Electrician", "HardwareStore"], "name": "Erencan Elektrik",
                      "telephone": TEL_INTL, "url": f"{SITE}/",
                      "address": {"@type": "PostalAddress", "streetAddress": "Beylikdüzü OSB Mah., Birlik Sanayi Sitesi 2. Cad. No:1/1 D:4",
                                  "addressLocality": "Beylikdüzü", "addressRegion": "İstanbul", "postalCode": "34524", "addressCountry": "TR"}},
         "areaServed": [{"@type": "City", "name": "İstanbul" if lang == "tr" else "Istanbul"},
                        {"@type": "Country", "name": "Türkiye"}]},
        breadcrumb_ld(lang, p["nav"], path),
        faq_ld(p["faq"]),
    ]
    blocks = []
    for title, kind, data in p["blocks"]:
        if kind == "brands" and data == "same":
            data = next(b for b in next(x for x in PAGES if x["slug"] == tr_slug)["blocks"] if b[1] == "brands")[2]
        blocks.append(block(title, kind, data))
    cta_h, cta_p = SERVICE_CTA[lang]
    return head(lang, p["title"], p["desc"], path, lds) + f'''<body>
{header(lang, path)}
<main id="icerik">
  <section class="page-head">
    <div class="wrap">
      {crumbs(lang, p["nav"])}
      <div class="page-title">{icon(tr_slug, 56)}<h1>{p["h1"]}</h1></div>
      <p class="lead">{p["lead"]}</p>
      {actions(lang, tr_slug)}
    </div>
  </section>

  <div class="wrap sub-body">
{chr(10).join(blocks)}
    <section class="sub-block">
      <h2>{t["faq_h"]}</h2>
      <div class="faq">
{faq(p["faq"])}
      </div>
    </section>
  </div>

{cta(lang, cta_h, cta_p, tr_slug)}

  <nav class="wrap others" aria-label="{t["others_label"]}">
    <h2>{t["others"]}</h2>
    <ul class="other-links">{others}</ul>
  </nav>
</main>
{footer(lang)}
</body>
</html>
'''


# ---------- teklif formu, KVKK/gizlilik ve teşekkür sayfaları ----------
def simple_page(lang, title, desc, path, main, crumb=None, lds=(), noindex=False):
    lds = list(lds)
    if crumb:
        lds.append(breadcrumb_ld(lang, crumb, path))
    return head(lang, title, desc, path, lds, noindex=noindex) + f'''<body>
{header(lang, path)}
<main id="icerik">
  <section class="page-head">
    <div class="wrap">
      {crumbs(lang, crumb) if crumb else ""}
{main}
</main>
{footer(lang)}
</body>
</html>
'''


# (data-konu, gönderilen değer [Türkçe, e-postada görünür], TR etiket, EN etiket)
KONULAR = [
    ("elektrik-malzemesi", "Elektrik malzemesi", "Elektrik malzemesi", "Electrical supplies"),
    ("toptan", "Toptan alım / cari hesap", "Toptan alım / cari hesap", "Wholesale / trade account"),
    ("pano-tasarim-montaj", "Pano tasarımı ve montajı", "Pano tasarımı ve montajı", "Panel design and installation"),
    ("elektrik-taahhut", "Elektrik taahhüdü / keşif", "Elektrik taahhüdü / keşif", "Electrical contracting / site survey"),
    ("proje-muhendislik", "Proje ve mühendislik", "Proje ve mühendislik", "Engineering and design"),
    ("diger", "Diğer", "Diğer", "Other"),
]

Q = {
    "tr": {
        "path": "/teklif-al/", "thanks": "/teklif-al/tesekkurler/",
        "title": "Elektrik Malzemesi ve Pano Teklifi Alın | Erencan Elektrik",
        "desc": "Elektrik malzemesi, pano, taahhüt ve proje işleriniz için online teklif isteyin. Malzeme listenizi yazın, Beylikdüzü'ndeki ekibimiz size dönsün.",
        "crumb": "Teklif al", "h1": "Teklif isteyin",
        "lead": "İhtiyacınızı kısaca yazın; malzeme için fiyat ve stok durumunu, pano ve taahhüt işleri için keşif ya da teklif bilgisini e-postayla veya telefonla iletelim.",
        "subject": "Yeni teklif talebi (erencanelektrik.com)", "lang_field": "Türkçe",
        "l_konu": "Konu", "l_ad": "Ad soyad", "l_firma": "Firma", "l_tel": "Telefon", "l_mail": "E-posta",
        "l_yer": "İl / ilçe", "l_talep": "Talebiniz", "opt": "(isteğe bağlı)", "yer_ph": "Örn. Esenyurt, İstanbul",
        "talep_ph": "Ürün, marka ve adetleri ya da yapılacak işi yazın. Malzeme listenizi buraya yapıştırabilirsiniz.",
        "hint": 'Şema, fotoğraf veya Excel listesi göndermek için <a href="mailto:{MAIL}?subject=Teklif%20talebi%20-%20ek%20dosya">{MAIL}</a> adresine e-posta atabilirsiniz.',
        "kvkk": '<a href="/kvkk/" target="_blank" rel="noopener">KVKK aydınlatma metnini</a> okudum; bilgilerimin teklif talebim için işlenmesini ve bu amaçla yurt dışındaki e-posta sunucularına aktarılmasını kabul ediyorum.',
        "send": "Teklif talebini gönder",
        "side_label": "Teklif için ipuçları", "side_h": "Ne yazmalısınız?",
        "tips": [("Malzeme", "Ürün adı, marka ve adet. Uzun bir listeyi olduğu gibi yapıştırabilirsiniz."),
                 ("Pano", "Pano tipi, giriş akımı ve çıkış sayısı. Tek hat şemanız varsa belirtin."),
                 ("Taahhüt", "İş yerinin türü, ilçesi ve yaklaşık büyüklüğü. Keşif ücretsizdir.")],
        "files_h": "Dosya göndermek için",
        "files": 'Şema, fotoğraf veya Excel listesini <a href="mailto:{MAIL}">{MAIL}</a> adresine ya da <a href="{WA}" rel="noopener">WhatsApp\'tan</a> gönderebilirsiniz.',
        "phone": "Telefon",
        "t_title": "Talebiniz alındı | Erencan Elektrik", "t_desc": "Teklif talebiniz Erencan Elektrik'e ulaştı.",
        "t_h1": "Talebiniz bize ulaştı",
        "t_lead": 'Teşekkürler. Talebinizi inceleyip mesai saatlerinde ({HOURS}) size dönüş yapacağız. Acil bir durum için <a href="tel:{TEL}">{TEL_TXT}</a> numarasından bize ulaşabilirsiniz.',
        "t_back": "Ana sayfaya dön",
    },
    "en": {
        "path": "/en/quote/", "thanks": "/en/quote/thank-you/",
        "title": "Request a Quote for Electrical Supplies & Panels | Erencan",
        "desc": "Request a quote for electrical supplies, panels, contracting or engineering. Send your material list and our team in Istanbul will reply.",
        "crumb": "Get a quote", "h1": "Request a quote",
        "lead": "Tell us briefly what you need. We will send you prices and stock for materials, or a survey and quotation for panel and contracting work, by email or phone.",
        "subject": "Yeni teklif talebi - İngilizce (erencanelektrik.com/en)", "lang_field": "İngilizce (English) - lütfen İngilizce yanıtlayın",
        "l_konu": "Subject", "l_ad": "Full name", "l_firma": "Company", "l_tel": "Phone", "l_mail": "Email",
        "l_yer": "City / district", "l_talep": "Your request", "opt": "(optional)", "yer_ph": "e.g. Esenyurt, Istanbul",
        "talep_ph": "List the products, brands and quantities, or describe the job. You can paste your material list here.",
        "hint": 'To send a drawing, photo or Excel list, email it to <a href="mailto:{MAIL}?subject=Quote%20request%20-%20attachment">{MAIL}</a>.',
        "kvkk": 'I have read the <a href="/en/privacy/" target="_blank" rel="noopener">privacy notice</a> and agree that my details are processed for my quote request and transferred to email servers abroad for this purpose.',
        "send": "Send quote request",
        "side_label": "Tips for your request", "side_h": "What to include",
        "tips": [("Materials", "Product name, brand and quantity. You can paste a long list as it is."),
                 ("Panels", "Panel type, incoming current and number of outgoing circuits. Mention it if you have a single-line diagram."),
                 ("Contracting", "Type of site, district and approximate size. The site survey is free.")],
        "files_h": "Sending files",
        "files": 'Send drawings, photos or Excel lists to <a href="mailto:{MAIL}">{MAIL}</a> or via <a href="{WA}" rel="noopener">WhatsApp</a>.',
        "phone": "Phone",
        "t_title": "Request received | Erencan Elektrik", "t_desc": "Your quote request has reached Erencan Elektrik.",
        "t_h1": "We have received your request",
        "t_lead": 'Thank you. We will review your request and get back to you during opening hours ({HOURS}). For anything urgent, call us on <a href="tel:{TEL}">{TEL_INTL}</a>.',
        "t_back": "Back to home page",
    },
}


def fill(s, lang):
    return (s.replace("{MAIL}", MAIL).replace("{WA}", WA).replace("{TEL_TXT}", TEL_TXT).replace("{TEL_INTL}", TEL_INTL)
             .replace("{TEL}", TEL).replace("{HOURS}", T[lang]["hours"]))


def teklif_page(lang):
    q, t = Q[lang], T[lang]
    opts = "".join(f'<option value="{val}" data-konu="{k}">{tr if lang == "tr" else en}</option>'
                   for k, val, tr, en in KONULAR)
    tips = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in q["tips"])
    opt = f'<span class="opt">{q["opt"]}</span>'
    main = f'''      <h1>{q["h1"]}</h1>
      <p class="lead">{q["lead"]}</p>
    </div>
  </section>

  <div class="wrap quote">
    <form class="quote-form" id="teklif-formu" action="https://api.web3forms.com/submit" method="POST" novalidate>
      <input type="hidden" name="access_key" value="{FORM_KEY}">
      <input type="hidden" name="subject" value="{q["subject"]}">
      <input type="hidden" name="from_name" value="Erencan Elektrik web sitesi">
      <input type="hidden" name="Dil" value="{q["lang_field"]}">
      <input type="hidden" name="redirect" value="{SITE}{q["thanks"]}">
      <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">

      <div class="field">
        <label for="f-konu">{q["l_konu"]}</label>
        <select id="f-konu" name="Konu" required>{opts}</select>
      </div>
      <div class="field-row">
        <div class="field">
          <label for="f-ad">{q["l_ad"]}</label>
          <input id="f-ad" name="Ad soyad" type="text" autocomplete="name" required>
        </div>
        <div class="field">
          <label for="f-firma">{q["l_firma"]} {opt}</label>
          <input id="f-firma" name="Firma" type="text" autocomplete="organization">
        </div>
      </div>
      <div class="field-row">
        <div class="field">
          <label for="f-tel">{q["l_tel"]}</label>
          <input id="f-tel" name="Telefon" type="tel" autocomplete="tel" inputmode="tel" required>
        </div>
        <div class="field">
          <label for="f-mail">{q["l_mail"]} {opt}</label>
          <input id="f-mail" name="email" type="email" autocomplete="email">
        </div>
      </div>
      <div class="field">
        <label for="f-yer">{q["l_yer"]} {opt}</label>
        <input id="f-yer" name="İl / ilçe" type="text" autocomplete="address-level2" placeholder="{q["yer_ph"]}">
      </div>
      <div class="field">
        <label for="f-talep">{q["l_talep"]}</label>
        <textarea id="f-talep" name="Talep" rows="8" required placeholder="{q["talep_ph"]}"></textarea>
        <p class="hint">{fill(q["hint"], lang)}</p>
      </div>
      <div class="field check">
        <input id="f-kvkk" name="KVKK" type="checkbox" value="Aydınlatma metnini okudu, onayladı" required>
        <label for="f-kvkk">{q["kvkk"]}</label>
      </div>
      <p class="form-status" id="form-durum" role="status" aria-live="polite"></p>
      <button class="btn" type="submit">{q["send"]}</button>
    </form>

    <aside class="quote-side" aria-label="{q["side_label"]}">
      <h2>{q["side_h"]}</h2>
      <dl class="tips">{tips}</dl>
      <h2>{q["files_h"]}</h2>
      <p>{fill(q["files"], lang)}</p>
      <p>{q["phone"]}: <a href="tel:{TEL}">{TEL_TXT if lang == "tr" else TEL_INTL}</a><br>{t["hours"]}</p>
    </aside>
  </div>'''
    lds = [{"@context": "https://schema.org", "@type": "ContactPage", "name": q["h1"], "inLanguage": lang,
            "url": f"{SITE}{q['path']}", "about": {"@id": f"{SITE}/#isletme"}}]
    return simple_page(lang, q["title"], q["desc"], q["path"], main, crumb=q["crumb"], lds=lds)


def tesekkur_page(lang):
    q, t = Q[lang], T[lang]
    main = f'''      <h1>{q["t_h1"]}</h1>
      <p class="lead">{fill(q["t_lead"], lang)}</p>
      <div class="actions"><a class="btn" href="{t["home"]}">{q["t_back"]}</a></div>
    </div>
  </section>'''
    return simple_page(lang, q["t_title"], q["t_desc"], q["thanks"], main, noindex=True)


def kvkk_page(lang):
    if lang == "tr":
        h1, lead, crumb = ("Kişisel verilerin korunması aydınlatma metni",
                           "Bu metin, teklif formu ve iletişim kanallarımız aracılığıyla bize ilettiğiniz kişisel verilerin 6698 sayılı Kişisel Verilerin Korunması Kanunu (KVKK) kapsamında nasıl işlendiğini açıklar.",
                           "KVKK aydınlatma metni")
        secs = [
            ("Veri sorumlusu", f'{TRADE}<br>{ADDR_LINE1}, {ADDR_LINE2}<br>E-posta: <a href="mailto:{MAIL}">{MAIL}</a><br>Telefon: <a href="tel:{TEL}">{TEL_TXT}</a>'),
            ("İşlenen kişisel veriler", "Teklif formunda paylaştığınız ad soyad, firma adı, telefon numarası, e-posta adresi, il/ilçe bilgisi ve talep metninize yazdığınız bilgiler."),
            ("İşleme amacı ve hukuki sebep", "Verileriniz yalnızca teklif talebinizi değerlendirmek, size fiyat ve teklif iletmek ve bu konuda sizinle iletişim kurmak amacıyla işlenir. Hukuki sebep, KVKK'nın 5. maddesinin 2. fıkrasının (c) bendi uyarınca bir sözleşmenin kurulmasıyla doğrudan ilgili olmasıdır."),
            ("Aktarım", "Form, e-posta iletimi için Web3Forms hizmetini kullanır ve talepler şirketimizin Gmail (Google) e-posta hesabına iletilir. Bu hizmet sağlayıcıların sunucuları yurt dışında bulunduğundan, formu gönderirken verdiğiniz açık rızaya dayanarak verileriniz yurt dışına aktarılır. Verileriniz bunun dışında üçüncü kişilerle paylaşılmaz, pazarlama amacıyla kullanılmaz."),
            ("Saklama süresi", "Teklif talepleri, talebin sonuçlanmasından ve ilgili yasal saklama yükümlülüklerinin sona ermesinden sonra silinir."),
            ("Haklarınız", f"KVKK'nın 11. maddesi uyarınca verilerinizin işlenip işlenmediğini öğrenme, bilgi talep etme, düzeltilmesini veya silinmesini isteme ve işlemeye itiraz etme haklarına sahipsiniz. Başvurularınızı <a href=\"mailto:{MAIL}\">{MAIL}</a> adresine iletebilirsiniz."),
        ]
        title, desc, path = ("KVKK Aydınlatma Metni | Erencan Elektrik",
                             "Erencan Elektrik teklif formu ve iletişim kanalları için kişisel verilerin korunması aydınlatma metni.", "/kvkk/")
    else:
        h1, lead, crumb = ("Privacy notice",
                           "This notice explains how we process the personal data you send us through the quote form and our contact channels, under Turkish Law No. 6698 on the Protection of Personal Data (KVKK).",
                           "Privacy notice")
        secs = [
            ("Data controller", f'{TRADE}<br>{ADDR_LINE1}, {ADDR_LINE2}<br>Email: <a href="mailto:{MAIL}">{MAIL}</a><br>Phone: <a href="tel:{TEL}">{TEL_INTL}</a>'),
            ("Data we process", "The name, company, phone number, email address, city/district and request details you enter in the quote form."),
            ("Purpose and legal basis", "We use your data only to assess your quote request, send you prices and quotations, and contact you about them. The legal basis is Article 5(2)(c) of the KVKK: processing directly related to entering into a contract."),
            ("Transfers", "The form uses the Web3Forms service to deliver messages, which arrive in our company's Gmail (Google) mailbox. Because these providers' servers are located outside Türkiye, your data is transferred abroad on the basis of the explicit consent you give when submitting the form. We do not share your data with any other third party or use it for marketing."),
            ("Retention", "Quote requests are deleted once the request is concluded and any legal retention obligations have expired."),
            ("Your rights", f"Under Article 11 of the KVKK you may ask whether your data is processed, request information, ask for correction or deletion, and object to processing. Send requests to <a href=\"mailto:{MAIL}\">{MAIL}</a>."),
        ]
        title, desc, path = ("Privacy Notice | Erencan Elektrik",
                             "Privacy notice for the Erencan Elektrik quote form and contact channels, under Turkish personal data protection law (KVKK).", "/en/privacy/")
    body = "\n".join(f"    <h2>{a}</h2>\n    <p>{b}</p>" for a, b in secs)
    main = f'''      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
    </div>
  </section>

  <div class="wrap narrow legal">
{body}
  </div>'''
    return simple_page(lang, title, desc, path, main, crumb=crumb)


# ---------- site haritası ----------
def sitemap(paths):
    rows = []
    for p in paths:
        alt = alt_of(p)
        tr_p, en_p = (p, alt) if lang_of(p) == "tr" else (alt, p)
        links = (f'\n    <xhtml:link rel="alternate" hreflang="tr" href="{SITE}{tr_p}"/>'
                 f'\n    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{en_p}"/>'
                 f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{tr_p}"/>')
        rows.append(f"  <url>\n    <loc>{SITE}{p}</loc>\n    <lastmod>{TODAY}</lastmod>{links}\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(rows) + "\n</urlset>\n")


def write(path, html):
    d = os.path.join(ROOT, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    out = {}
    for lang in ("tr", "en"):
        out[T[lang]["home"]] = home(lang)
        for p in (PAGES if lang == "tr" else PAGES_EN):
            out[f"/{p['slug']}/"] = service_page(lang, p)
        out[Q[lang]["path"]] = teklif_page(lang)
        out[Q[lang]["thanks"]] = tesekkur_page(lang)
        out[T[lang]["privacy"]] = kvkk_page(lang)
    for path, html in out.items():
        write(path, html)
    indexable = [p for p in out if "tesekkurler" not in p and "thank-you" not in p]
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap(indexable))
    print(f"{len(out)} sayfa yazıldı, site haritasında {len(indexable)} adres")
