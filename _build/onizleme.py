"""Ana sayfa tasarım önizlemeleri (yayındaki siteyi değiştirmez).

python3 _build/onizleme.py  ->  onizleme/1/ ve onizleme/2/ (noindex)
"""
import os
import re

import build_site as B

ICONS = {
    # sigorta (otomat)
    "elektrik-malzemesi": '<rect x="14" y="6" width="20" height="36" rx="2"/><path d="M14 14h20M14 34h20"/><rect x="20" y="19" width="8" height="10" rx="1"/><path d="M24 19v-3"/>',
    # pano dolabı
    "pano-tasarim-montaj": '<rect x="9" y="5" width="30" height="38" rx="2"/><path d="M24 5v38"/><path d="M14 13h5M14 19h5M29 13h5M29 19h5"/><circle cx="21" cy="28" r="1.2"/><circle cx="27" cy="28" r="1.2"/>',
    # bina + yıldırım
    "elektrik-taahhut": '<path d="M7 43V17l12-8 12 8v26"/><path d="M3 43h42"/><path d="M31 25h10v18"/><path d="M20 20l-4 9h6l-3 8"/>',
    # proje paftası
    "proje-muhendislik": '<path d="M9 7h22l8 8v26H9z"/><path d="M31 7v8h8"/><path d="M15 23h18M15 29h18M15 35h10"/>',
}


def icon(slug, cls="ico"):
    return (f'<svg class="{cls}" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[slug]}</svg>')


def head(v):
    h = B.home().split("<body>")[0]
    h = h.replace('<link rel="icon"', f'<link rel="stylesheet" href="/onizleme/ortak.css?v={B.V}">\n  <link rel="stylesheet" href="/onizleme/v{v}.css?v={B.V}">\n  <link rel="icon"', 1)
    h = re.sub(r'<link rel="canonical"[^>]*>', '<meta name="robots" content="noindex, nofollow">', h)
    return h


def services_cards():
    return "\n".join(f'''        <li>
          <a href="/{slug}/">
            {icon(slug)}
            <h3>{name}</h3>
            <p>{desc}</p>
            <span class="more">Hizmeti inceleyin</span>
          </a>
        </li>''' for slug, name, desc in B.HOME_SERVICES)


def common_tail():
    brands = B.marquee(B.LISTS["markalar"], "Satışını yaptığımız markalar")
    refs = B.marquee(B.LISTS["referanslar"], "Referans firmalar", speed=32, size=.9)
    return brands, refs


def faq_block(cls=""):
    return f'''  <section class="block faq-split {cls}" id="sss">
    <div class="wrap faq-grid">
      <div class="faq-head">
        <h2>Sıkça sorulan sorular</h2>
        <p>Aradığınızı bulamadıysanız <a href="/teklif-al/">teklif formundan</a> yazın ya da <a href="tel:{B.TEL}">arayın</a>.</p>
      </div>
      <div class="faq">
{B.faq(B.HOME_FAQ)}
      </div>
    </div>
  </section>'''


def contact_block():
    return f'''  <section class="block block-steel" id="iletisim">
    <div class="wrap contact">
      <div>
        <h2>İletişim</h2>
        <dl class="contact-list">
          <div><dt>Adres</dt><dd><address>{B.ADDR_LINE1}<br>{B.ADDR_LINE2}</address><a href="{B.MAPS}" rel="noopener">Google Haritalar'da aç</a></dd></div>
          <div><dt>Telefon ve WhatsApp</dt><dd><a href="tel:{B.TEL}">{B.TEL_TXT}</a></dd></div>
          <div><dt>E-posta</dt><dd><a href="mailto:{B.MAIL}">{B.MAIL}</a></dd></div>
          <div><dt>Çalışma saatleri</dt><dd>{B.HOURS}</dd></div>
          <div><dt>Hizmet bölgesi</dt><dd>Beylikdüzü merkezli, İstanbul geneli. Malzeme gönderimi Türkiye geneline.</dd></div>
        </dl>
        {B.actions()}
        <p class="review-note">Bizimle çalıştıysanız <a href="{B.REVIEW}" rel="noopener">Google'da değerlendirmenizi</a> bekleriz.</p>
      </div>
      <iframe class="map" title="Erencan Elektrik konumu" src="{B.MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
  </section>'''


def cta(title, text):
    return f'''  <section class="cta-band">
    <div class="wrap cta-inner">
      <div>
        <h2>{title}</h2>
        <p>{text}</p>
      </div>
      <div class="cta-actions">
        <a class="btn btn-light" href="/teklif-al/">Teklif isteyin</a>
        <a class="btn btn-ghost" href="{B.WA}" rel="noopener">WhatsApp'tan yazın</a>
      </div>
    </div>
  </section>'''


def page(v, main):
    return head(v) + f'''<body class="v{v}">
{B.header()}
<main id="icerik">
{main}
</main>
{B.footer()}
</body>
</html>
'''


# ---------- 1: Mağaza (fotoğraf ağırlıklı) ----------
def v1():
    brands, refs = common_tail()
    main = f'''  <section class="hero1">
    <picture class="hero1-photo">
      <source media="(max-width: 900px)" srcset="/assets/vitrin-900.webp?v={B.V}">
      <img src="/assets/vitrin.webp?v={B.V}" width="1536" height="1044" alt="Erencan Elektrik'in Birlik Sanayi Sitesi'ndeki mağazası" fetchpriority="high">
    </picture>
    <div class="wrap hero1-inner">
      <p class="hero1-kicker">Birlik Sanayi Sitesi, Beylikdüzü</p>
      <h1>Elektrik malzemesi, pano ve taahhüt işleri tek adreste</h1>
      <p class="lead">2004'ten beri şalt, kablo ve pano malzemesi satıyor; fabrika, ticari yapı ve konut projelerinin elektrik işlerini üstleniyoruz.</p>
      <div class="actions">
        <a class="btn btn-light" href="/teklif-al/">Teklif isteyin</a>
        <a class="btn btn-ghost" href="{B.WA}" rel="noopener">WhatsApp'tan yazın</a>
      </div>
    </div>
  </section>
  <div class="facts-wrap">
    <div class="wrap">{B.plate()}</div>
  </div>

  <section class="block" id="hizmetler">
    <div class="wrap">
      <h2>Hizmetlerimiz</h2>
      <ul class="cards">
{services_cards()}
      </ul>
    </div>
  </section>

  <section class="photo-band">
    <img src="/assets/hakkimizda2.webp?v={B.V}" width="900" height="1200" alt="" loading="lazy" decoding="async">
    <div class="wrap photo-band-inner">
      <p class="big">Şalt, kablo ve pano malzemesi raflarımızda. Tek sigortadan proje siparişine kadar.</p>
      <ul class="figures">
        <li><strong>2004</strong><span>yılından beri Beylikdüzü'nde</span></li>
        <li><strong>{len(B.LISTS["markalar"])}</strong><span>markanın ürünleri stokta</span></li>
        <li><strong>Türkiye</strong><span>geneline malzeme gönderimi</span></li>
      </ul>
    </div>
  </section>

  <section class="block" id="markalar">
    <div class="wrap">
      <h2>Satışını yaptığımız markalar</h2>
      <p class="section-note">Bu markaların ürünleri mağazamızda stokta.</p>
      {brands}
    </div>
  </section>

  <section class="block block-steel" id="referanslar">
    <div class="wrap">
      <h2>Çalıştığımız firmalardan bazıları</h2>
      {refs}
    </div>
  </section>

  <section class="block" id="hakkimizda">
    <div class="wrap about1">
      <div class="about1-photos">
        <img src="/assets/hakkimizda3.webp?v={B.V}" width="900" height="1200" alt="Stoktaki kablo makaraları ve pano malzemeleri" loading="lazy" decoding="async">
        <img src="/assets/hakkimizda1.webp?v={B.V}" width="900" height="1200" alt="Erencan Elektrik mağaza cephesi" loading="lazy" decoding="async">
      </div>
      <div class="about-text">
        <h2>Hakkımızda</h2>
        <p>Erencan Elektrik 2004 yılında Beylikdüzü'nde kuruldu. Endüstriyel elektrik sistemleri ve projelendirme alanında çalışan kadromuzla Türkiye'nin birçok bölgesinde bireysel ve kurumsal müşterilere hizmet verdik.</p>
        <p>Alçak gerilim sistemleri, pano kurulumu, bina içi tesisat ve dış saha uygulamalarını standartlara uygun malzemeyle yapıyoruz. Malzemeyi kendi stoğumuzdan sağladığımız için projeyi baştan sona tek elden yürütebiliyoruz.</p>
      </div>
    </div>
  </section>

{cta("Malzeme listenizi gönderin, fiyatını çıkaralım", "Ürün, marka ve adetleri yazmanız yeterli. Firmalara toptan fiyat ve cari hesap açıyoruz.")}

{faq_block()}

{contact_block()}'''
    return page(1, main)


# ---------- 2: Şalt panosu (grafik, teknik) ----------
def v2():
    brands, refs = common_tail()
    modules = "\n".join(f'''        <li>
          <a href="/{slug}/">
            <span class="mod-top">{icon(slug)}</span>
            <h3>{name}</h3>
            <p>{desc}</p>
            <span class="more">Detaylar</span>
          </a>
        </li>''' for slug, name, desc in B.HOME_SERVICES)
    main = f'''  <section class="hero hero2">
    <div class="hero-panel">
      <div class="hero-inner">
        <h1>Beylikdüzü'nde elektrik malzemesi, pano ve taahhüt</h1>
        <p class="lead">Birlik Sanayi Sitesi'ndeki mağazamızda 2004'ten beri şalt, kablo ve pano malzemesi satıyor; fabrika, ticari yapı ve konut projelerinin elektrik işlerini üstleniyoruz.</p>
        <div class="actions">
          <a class="btn btn-light" href="/teklif-al/">Teklif isteyin</a>
          <a class="btn btn-ghost" href="tel:{B.TEL}" aria-label="Bizi arayın: {B.TEL_TXT}">Bizi arayın</a>
        </div>
      </div>
    </div>
    <picture class="hero-photo">
      <source media="(max-width: 900px)" srcset="/assets/vitrin-900.webp?v={B.V}">
      <img src="/assets/vitrin.webp?v={B.V}" width="1536" height="1044" alt="Erencan Elektrik'in Birlik Sanayi Sitesi'ndeki mağazası" fetchpriority="high">
    </picture>
  </section>
  <div class="facts-wrap">
    <div class="wrap">{B.plate()}</div>
  </div>

  <section class="block rail-block" id="hizmetler">
    <div class="wrap">
      <h2>Hizmetlerimiz</h2>
      <ul class="rail">
{modules}
      </ul>
    </div>
  </section>

  <section class="block" id="surec">
    <div class="wrap">
      <h2>Teklif nasıl ilerliyor?</h2>
      <ol class="flow">
        <li><strong>Talebinizi iletin</strong><span>Malzeme listenizi, pano ihtiyacınızı ya da işi formdan, telefondan veya WhatsApp'tan yazın.</span></li>
        <li><strong>Teklifi alın</strong><span>Malzemede fiyat ve stok durumunu, pano ve taahhütte keşif sonrası teklifi iletiyoruz. Keşif ücretsiz.</span></li>
        <li><strong>Teslim ve uygulama</strong><span>Malzemeyi mağazadan teslim ediyor ya da kargoluyoruz; panoyu onaydan sonra imal edip sahada kuruyoruz.</span></li>
      </ol>
    </div>
  </section>

  <section class="block block-steel" id="markalar">
    <div class="wrap">
      <h2>Satışını yaptığımız markalar</h2>
      <p class="section-note">Bu markaların ürünleri mağazamızda stokta.</p>
      {brands}
    </div>
  </section>

  <section class="block" id="referanslar">
    <div class="wrap">
      <h2>Çalıştığımız firmalardan bazıları</h2>
      {refs}
    </div>
  </section>

  <section class="block block-steel about2" id="hakkimizda">
    <div class="wrap about2-grid">
      <div class="about-text">
        <h2>Hakkımızda</h2>
        <p>Erencan Elektrik 2004 yılında Beylikdüzü'nde kuruldu. Endüstriyel elektrik sistemleri ve projelendirme alanında çalışan kadromuzla Türkiye'nin birçok bölgesinde bireysel ve kurumsal müşterilere hizmet verdik.</p>
        <p>Alçak gerilim sistemleri, pano kurulumu, bina içi tesisat ve dış saha uygulamalarını standartlara uygun malzemeyle yapıyoruz. Malzemeyi kendi stoğumuzdan sağladığımız için projeyi baştan sona tek elden yürütebiliyoruz.</p>
      </div>
      <div class="mosaic">
        <img class="m1" src="/assets/hakkimizda2.webp?v={B.V}" width="900" height="1200" alt="Mağazadaki elektrik malzemesi rafları" loading="lazy" decoding="async">
        <img class="m2" src="/assets/hakkimizda3.webp?v={B.V}" width="900" height="1200" alt="Stoktaki kablo makaraları ve pano malzemeleri" loading="lazy" decoding="async">
        <img class="m3" src="/assets/hakkimizda1.webp?v={B.V}" width="900" height="1200" alt="Erencan Elektrik mağaza cephesi" loading="lazy" decoding="async">
      </div>
    </div>
  </section>

{cta("Projeniz için fiyat alın", "Malzeme listesi, pano ya da taahhüt işi: talebinizi gönderin, mesai saatlerinde dönelim.")}

{faq_block()}

{contact_block()}'''
    return page(2, main)


if __name__ == "__main__":
    for v, fn in ((1, v1), (2, v2)):
        d = os.path.join(B.ROOT, "onizleme", str(v))
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(fn())
    print("önizlemeler yazıldı")
