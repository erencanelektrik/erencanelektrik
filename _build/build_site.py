"""Erencan Elektrik sitesini üretir.

Kullanım (repo kökünden):  python3 _build/build_site.py
Ana sayfa (index.html) ve dört hizmet sayfası ortak üst menü / alt bilgi ile
yeniden yazılır. Hizmet metinleri pages_data.py, logo listeleri
logo_lists.json, ana sayfanın <head> kısmı head_home.html içindedir.
_build klasörü GitHub Pages tarafından yayınlanmaz.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
V = "8"  # önbellek sürümü: CSS/JS/görsel değişince artırın

from pages_data import PAGES  # noqa: E402

SITE = "https://erencanelektrik.com"
TEL = "+905325861860"
TEL_TXT = "0532 586 18 60"
WA = "https://wa.me/905325861860"
MAIL = "erencanelektrik@gmail.com"
ADDR_LINE1 = "Beylikdüzü OSB Mah., Birlik Sanayi Sitesi"
ADDR_LINE2 = "2. Cad. No:1/1 D:4, 34524 Beylikdüzü / İstanbul"
MAPS = "https://maps.app.goo.gl/eDhi7KrXCUre3yDB6"
MAP_EMBED = ("https://maps.google.com/maps?q=Erencan+Elektrik,+Birlik+Sanayi+Sitesi,"
             "+Beylikd%C3%BCz%C3%BC,+%C4%B0stanbul&z=16&output=embed")
HOURS = "Pazartesi–Cumartesi 08:00–19:00, pazar kapalı"

LOGOS = json.load(open(os.path.join(HERE, "logos.json"), encoding="utf-8"))
BY_STEM = {os.path.splitext(os.path.basename(v["file"]))[0]: v for v in LOGOS.values()}
LISTS = json.load(open(os.path.join(HERE, "logo_lists.json"), encoding="utf-8"))

FONT = ('<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/archivo-latin-wdth-normal.woff2" crossorigin>\n'
        '  <link rel="preload" as="font" type="font/woff2" href="/assets/fonts/archivo-latin-ext-wdth-normal.woff2" crossorigin>')

NAV = [("Hizmetler", "/#hizmetler"), ("Markalar", "/#markalar"), ("Referanslar", "/#referanslar"),
       ("Hakkımızda", "/#hakkimizda"), ("SSS", "/#sss"), ("İletişim", "/#iletisim")]


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


def header(current=None):
    links = "".join(
        f'<li><a href="{href}"{" aria-current=\"page\"" if current == href else ""}>{name}</a></li>'
        for name, href in NAV)
    return f'''<a class="skip" href="#icerik">İçeriğe geç</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="/" aria-label="Erencan Elektrik ana sayfa">
      <img src="/assets/logo.webp?v={V}" alt="" width="60" height="60">
      <span>Erencan Elektrik</span>
    </a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-menu">Menü</button>
    <nav aria-label="Ana menü">
      <ul class="menu" id="site-menu">{links}</ul>
    </nav>
    <a class="bar-tel" href="tel:{TEL}" aria-label="Bizi arayın: {TEL_TXT}">Bizi arayın</a>
  </div>
</header>'''


def footer():
    services = "".join(f'<li><a href="/{p["slug"]}/">{p["nav"]}</a></li>' for p in PAGES)
    return f'''<footer class="site-footer">
  <div class="wrap foot">
    <div>
      <p class="foot-name">Erencan Elektrik İnşaat Taahhüt San. ve Tic. Ltd. Şti.</p>
      <p>{ADDR_LINE1}<br>{ADDR_LINE2}</p>
      <p><a href="tel:{TEL}">{TEL_TXT}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p>
    </div>
    <div>
      <p class="foot-h">Hizmetler</p>
      <ul>{services}</ul>
    </div>
    <div>
      <p class="foot-h">Çalışma saatleri</p>
      <p>{HOURS}</p>
      <p><a href="https://instagram.com/erencanelektrik" rel="noopener">Instagram</a></p>
    </div>
  </div>
  <p class="wrap copy">© 2026 Erencan Elektrik</p>
</footer>
<div class="quickbar" aria-label="Hızlı iletişim">
  <a href="tel:{TEL}">Ara</a>
  <a href="{WA}" rel="noopener">WhatsApp</a>
</div>
<script src="/app.js?v={V}" defer></script>'''


def plate():
    rows = [("Kuruluş", "2004, Beylikdüzü"),
            ("Satış", "Perakende ve toptan"),
            ("Gönderim", "Türkiye'nin her yerine"),
            ("Açık", "Pzt–Cmt 08:00–19:00")]
    cells = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows)
    return f'<dl class="facts" aria-label="Firma bilgileri">{cells}</dl>'


def faq(items):
    return "\n".join(f'''      <details>
        <summary>{q}</summary>
        <p>{a}</p>
      </details>''' for q, a in items)


def actions():
    return f'''<div class="actions">
        <a class="btn" href="{WA}" rel="noopener">WhatsApp'tan yazın</a>
        <a class="btn btn-line" href="tel:{TEL}" aria-label="Bizi arayın: {TEL_TXT}">Bizi arayın</a>
      </div>'''


# ---------- ana sayfa ----------
HOME_SERVICES = [
    ("elektrik-malzemesi", "Elektrik malzemesi satışı",
     "Şalt, kablo, bağlantı ve pano malzemeleri stokta. Tek parça da satıyoruz, firmalara toptan fiyat ve cari hesap açıyoruz."),
    ("pano-tasarim-montaj", "Pano tasarımı ve montajı",
     "IEC standartlarında endüstriyel ve bina tipi panolar. Teklifi onayladığınızda imalata başlıyoruz."),
    ("elektrik-taahhut", "Elektrik taahhüdü",
     "Fabrika, ticari yapı ve konut projelerinde alçak gerilim, bina içi tesisat ve dış saha uygulamaları. Keşif ücretsiz."),
    ("proje-muhendislik", "Proje ve mühendislik",
     "Yük hesapları, projelendirme ve teknik şartname uyumu. Projeyi hazırlayan ekip sahada da uyguluyor."),
]

HOME_FAQ = [
    ("Tek parça (perakende) malzeme alabilir miyim?", "Evet. Mağazamızda hem perakende hem toptan satış yapıyoruz; tek bir sigortadan büyük proje siparişlerine kadar malzeme temin edebilirsiniz."),
    ("Toptan alan firmalara özel fiyat veya cari hesap imkânı var mı?", "Evet. Düzenli ve toptan alım yapan firmalara özel fiyat ve cari hesap imkânı sunuyoruz. Detaylar için bizimle iletişime geçebilirsiniz."),
    ("Hangi markaların ürünlerini satıyorsunuz?", "Siemens, Schneider Electric, Legrand, Viko, Entes, Emas, Omron, Finder, Philips, Nexans, Borsan ve Öznur başta olmak üzere sektörün önde gelen markalarının şalt, kablo, aydınlatma ve pano malzemelerini satıyoruz."),
    ("Malzeme teslimatı veya kargo yapıyor musunuz?", "Evet. Türkiye'nin her yerine malzeme gönderimi yapıyoruz."),
    ("Pano siparişinde süreç nasıl işliyor?", "İhtiyacınıza göre teklif hazırlıyoruz; teklif onaylandıktan sonra panonun imalatına başlıyoruz. Teslim süresi panonun tipine ve büyüklüğüne göre değişir; net süreyi teklif aşamasında bildiriyoruz."),
    ("Elektrik taahhüt işlerinde keşif ücretli mi?", "Hayır, keşif ücretsizdir."),
    ("Hangi bölgelere hizmet veriyorsunuz?", "Beylikdüzü merkezli olarak İstanbul genelinde hizmet veriyoruz. İstanbul dışındaki projelere de iş ve malzeme gönderimi yapıyoruz."),
    ("Ödeme seçenekleri nelerdir?", "Nakit, kredi kartı ve havale/EFT ile ödeme kabul ediyoruz."),
    ("Ürünlerde garanti nasıl işliyor?", "Sattığımız tüm ürünlerde üretici firmanın garanti koşulları geçerlidir."),
    ("Çalışma saatleriniz nedir, nasıl teklif alabilirim?", "Pazartesi–Cumartesi 08:00–19:00 arası açığız, pazar günü kapalıyız. Teklif için 0532 586 18 60 numarasından arayabilir veya WhatsApp'tan yazabilirsiniz."),
]


def home():
    head = open(os.path.join(HERE, "head_home.html"), encoding="utf-8").read()
    # eski font/stil/ön yükleme bağlantılarını temizle, yenilerini ekle
    head = re.sub(r'\s*<link rel="preconnect"[^>]*>', "", head)
    head = re.sub(r'\s*<link rel="stylesheet"[^>]*>', "", head)
    head = re.sub(r'\s*<link rel="preload"[^>]*>', "", head)
    head = re.sub(r'<meta name="theme-color" content="[^"]*">', '<meta name="theme-color" content="#093b6f">', head)
    head = head.replace("</title>", f'</title>\n  <link rel="preload" as="image" href="/assets/vitrin.webp?v={V}" fetchpriority="high" media="(min-width: 901px)">\n  <link rel="preload" as="image" href="/assets/vitrin-900.webp?v={V}" fetchpriority="high" media="(max-width: 900px)">', 1)
    head = head.replace('<link rel="icon"', f'{FONT}\n  <link rel="stylesheet" href="/style.css?v={V}">\n  <link rel="icon"', 1)

    services = "\n".join(f'''      <li>
        <h3><a href="/{slug}/">{name}</a></h3>
        <p>{desc}</p>
      </li>''' for slug, name, desc in HOME_SERVICES)
    brands = "".join(f"<li>{logo(f, alt)}</li>" for alt, f in LISTS["markalar"])
    refs = "".join(f"<li>{logo(f, alt, .9)}</li>" for alt, f in LISTS["referanslar"])

    body = f'''<body>
{header()}
<main id="icerik">
  <section class="hero">
    <div class="hero-panel">
      <div class="hero-inner">
        <h1>Beylikdüzü'nde elektrik malzemesi, pano ve taahhüt</h1>
        <p class="lead">Birlik Sanayi Sitesi'ndeki mağazamızda 2004'ten beri şalt, kablo ve pano malzemesi satıyor; fabrika, ticari yapı ve konut projelerinin elektrik işlerini üstleniyoruz.</p>
        <div class="actions">
          <a class="btn btn-light" href="{WA}" rel="noopener">WhatsApp'tan yazın</a>
          <a class="btn btn-ghost" href="tel:{TEL}" aria-label="Bizi arayın: {TEL_TXT}">Bizi arayın</a>
        </div>
      </div>
    </div>
    <picture class="hero-photo">
      <source media="(max-width: 900px)" srcset="/assets/vitrin-900.webp?v={V}">
      <img src="/assets/vitrin.webp?v={V}" width="1536" height="1044" alt="Erencan Elektrik'in Birlik Sanayi Sitesi'ndeki mağazası" fetchpriority="high">
    </picture>
  </section>
  <div class="facts-wrap">
    <div class="wrap">{plate()}</div>
  </div>

  <section class="block" id="hizmetler">
    <div class="wrap">
      <h2>Hizmetlerimiz</h2>
      <ul class="services">
{services}
      </ul>
    </div>
  </section>

  <section class="block block-steel" id="markalar">
    <div class="wrap">
      <h2>Satışını yaptığımız markalar</h2>
      <p class="section-note">Bu markaların ürünleri mağazamızda stokta. Aradığınız ürün yoksa sipariş üzerine getiriyoruz.</p>
      {marquee(LISTS["markalar"], "Satışını yaptığımız markalar")}
    </div>
  </section>

  <section class="block" id="referanslar">
    <div class="wrap">
      <h2>Çalıştığımız firmalardan bazıları</h2>
      {marquee(LISTS["referanslar"], "Referans firmalar", speed=32, size=.9)}
    </div>
  </section>

  <section class="block block-steel" id="hakkimizda">
    <div class="wrap about">
      <div class="about-text">
        <h2>Hakkımızda</h2>
        <p>Erencan Elektrik 2004 yılında Beylikdüzü'nde kuruldu. Endüstriyel elektrik sistemleri ve projelendirme alanında çalışan kadromuzla Türkiye'nin birçok bölgesinde bireysel ve kurumsal müşterilere hizmet verdik.</p>
        <p>Alçak gerilim sistemleri, pano kurulumu, bina içi tesisat ve dış saha uygulamalarını standartlara uygun malzemeyle yapıyoruz. Malzemeyi kendi stoğumuzdan sağladığımız için projeyi baştan sona tek elden yürütebiliyoruz.</p>
      </div>
      <div class="about-photos">
        <img src="/assets/hakkimizda2.webp?v={V}" width="900" height="1200" alt="Mağazadaki elektrik malzemesi rafları" loading="lazy" decoding="async">
        <img src="/assets/hakkimizda3.webp?v={V}" width="900" height="1200" alt="Stoktaki şalt ve pano malzemeleri" loading="lazy" decoding="async">
      </div>
    </div>
  </section>

  <section class="block" id="sss">
    <div class="wrap narrow">
      <h2>Sıkça sorulan sorular</h2>
      <div class="faq">
{faq(HOME_FAQ)}
      </div>
    </div>
  </section>

  <section class="block block-steel" id="iletisim">
    <div class="wrap contact">
      <div>
        <h2>İletişim</h2>
        <dl class="contact-list">
          <div><dt>Adres</dt><dd><address>{ADDR_LINE1}<br>{ADDR_LINE2}</address><a href="{MAPS}" rel="noopener">Google Haritalar'da aç</a></dd></div>
          <div><dt>Telefon ve WhatsApp</dt><dd><a href="tel:{TEL}">{TEL_TXT}</a></dd></div>
          <div><dt>E-posta</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
          <div><dt>Çalışma saatleri</dt><dd>{HOURS}</dd></div>
          <div><dt>Hizmet bölgesi</dt><dd>Beylikdüzü merkezli, İstanbul geneli. Malzeme gönderimi Türkiye geneline.</dd></div>
        </dl>
        {actions()}
      </div>
      <iframe class="map" title="Erencan Elektrik konumu" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
  </section>
</main>
{footer()}
</body>
</html>
'''
    return head + body


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


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def service_page(p):
    url = f"{SITE}/{p['slug']}/"
    others = "".join(f'<li><a href="/{o["slug"]}/">{o["nav"]}</a></li>' for o in PAGES if o is not p)
    ld = [
        {"@context": "https://schema.org", "@type": "Service", "name": p["h1"], "serviceType": p["service_type"],
         "description": p["desc"], "url": url,
         "provider": {"@id": f"{SITE}/#isletme", "@type": ["Electrician", "HardwareStore"], "name": "Erencan Elektrik",
                      "telephone": "+90 532 586 18 60", "url": f"{SITE}/",
                      "address": {"@type": "PostalAddress", "streetAddress": "Beylikdüzü OSB Mah., Birlik Sanayi Sitesi 2. Cad. No:1/1 D:4",
                                  "addressLocality": "Beylikdüzü", "addressRegion": "İstanbul", "postalCode": "34524", "addressCountry": "TR"}},
         "areaServed": [{"@type": "City", "name": "İstanbul"}, {"@type": "Country", "name": "Türkiye"}]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": p["nav"], "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]},
    ]
    ld_html = "\n".join('  <script type="application/ld+json">\n' + json.dumps(x, ensure_ascii=False, indent=2) + "\n  </script>" for x in ld)
    blocks = "\n".join(block(*b) for b in p["blocks"])
    return f'''<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{esc(p["title"])}</title>
  <meta name="description" content="{esc(p["desc"])}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#093b6f">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="tr_TR">
  <meta property="og:site_name" content="Erencan Elektrik">
  <meta property="og:title" content="{esc(p["title"])}">
  <meta property="og:description" content="{esc(p["desc"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/hakkimizda1.jpg">
  {FONT}
  <link rel="stylesheet" href="/style.css?v={V}">
  <link rel="icon" type="image/x-icon" href="/assets/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32x32.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
{ld_html}
</head>
<body>
{header()}
<main id="icerik">
  <section class="page-head">
    <div class="wrap">
      <nav class="crumbs" aria-label="Sayfa konumu"><a href="/">Ana sayfa</a><span aria-hidden="true">/</span><span aria-current="page">{p["nav"]}</span></nav>
      <h1>{p["h1"]}</h1>
      <p class="lead">{p["lead"]}</p>
      {actions()}
    </div>
  </section>

  <div class="wrap sub-body">
{blocks}
    <section class="sub-block">
      <h2>Sıkça sorulan sorular</h2>
      <div class="faq">
{faq(p["faq"])}
      </div>
    </section>
    <section class="sub-block sub-contact">
      <h2>Teklif almak için</h2>
      <p>Pazartesi–Cumartesi 08:00–19:00 arası arayabilir ya da WhatsApp'tan yazabilirsiniz. Mağazamız {ADDR_LINE1}, {ADDR_LINE2} adresinde.</p>
      {actions()}
    </section>
    <nav class="sub-block" aria-label="Diğer hizmetler">
      <h2>Diğer hizmetlerimiz</h2>
      <ul class="other-links">{others}</ul>
    </nav>
  </div>
</main>
{footer()}
</body>
</html>
'''


if __name__ == "__main__":
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(home())
    for p in PAGES:
        d = os.path.join(ROOT, p["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(service_page(p))
    print("5 sayfa yazıldı")
