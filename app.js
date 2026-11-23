// Mobil menü
const btn = document.querySelector('.menu-btn');
const nav = document.querySelector('.site-header nav');

if (btn && nav) {
  const setOpen = (open) => {
    nav.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', String(open));
    btn.textContent = open ? (btn.dataset.close || 'Kapat') : (btn.dataset.open || 'Menü');
  };
  btn.addEventListener('click', () => setOpen(!nav.classList.contains('open')));
  nav.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => setOpen(false)));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setOpen(false); });
}

// Teklif formu
const form = document.getElementById('teklif-formu');

if (form) {
  const status = document.getElementById('form-durum');
  const submit = form.querySelector('button[type="submit"]');
  const en = document.documentElement.lang === 'en';
  const M = en ? {
    kvkk: 'Please accept the privacy notice to send your request.',
    fill: 'Please fill in the highlighted fields.',
    mail: 'Please check your email address.',
    sending: 'Sending…',
    ok: 'We have received your request and will get back to you during opening hours.',
    err: 'Your request could not be sent. Please try again or call us on +90 532 586 18 60.',
  } : {
    kvkk: 'Göndermek için KVKK aydınlatma metnini onaylayın.',
    fill: 'Lütfen işaretli alanları doldurun.',
    mail: 'E-posta adresini kontrol edin.',
    sending: 'Gönderiliyor…',
    ok: 'Talebiniz bize ulaştı. Mesai saatlerinde size dönüş yapacağız.',
    err: 'Gönderilemedi. Lütfen tekrar deneyin ya da 0532 586 18 60 numarasından bize ulaşın.',
  };
  const say = (text, kind) => { status.textContent = text; status.className = 'form-status ' + (kind || ''); };

  // Hizmet sayfasından gelindiyse konuyu seç (?konu=pano-tasarim-montaj)
  const konu = new URLSearchParams(location.search).get('konu');
  if (konu) {
    const opt = form.querySelector(`option[data-konu="${CSS.escape(konu)}"]`);
    if (opt) opt.selected = true;
  }

  form.querySelectorAll('[required]').forEach((el) =>
    el.addEventListener('input', () => el.removeAttribute('aria-invalid')));

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const missing = [...form.querySelectorAll('[required]')].filter((el) =>
      el.type === 'checkbox' ? !el.checked : !el.value.trim());
    const mail = form.querySelector('input[type="email"]');
    form.querySelectorAll('[aria-invalid]').forEach((el) => el.removeAttribute('aria-invalid'));
    missing.forEach((el) => el.setAttribute('aria-invalid', 'true'));
    if (missing.length) {
      const first = missing[0];
      say(first.type === 'checkbox' ? M.kvkk : M.fill, 'err');
      first.focus();
      return;
    }
    if (mail.value && !mail.checkValidity()) {
      mail.setAttribute('aria-invalid', 'true');
      say(M.mail, 'err');
      mail.focus();
      return;
    }

    const data = Object.fromEntries(new FormData(form));
    delete data.redirect;
    submit.disabled = true;
    say(M.sending);
    try {
      const res = await fetch(form.action, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(data),
      });
      const out = await res.json();
      if (!res.ok || !out.success) throw new Error(out.message || res.status);
      form.reset();
      say(M.ok, 'ok');
    } catch (err) {
      say(M.err, 'err');
    } finally {
      submit.disabled = false;
    }
  });
}

// Ana başlık daktilo efekti. Metin HTML'de olduğu gibi durur (arama motorları ve
// ekran okuyucular tam metni görür); burada yalnızca harfler sırayla görünür olur.
const typeH1 = document.querySelector('.type-h1');
if (typeH1) {
  const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (still) {
    typeH1.classList.add('ready');
  } else {
    const text = typeH1.textContent;
    typeH1.setAttribute('aria-label', text);
    typeH1.textContent = '';
    const chars = [...text].map((c) => {
      const s = document.createElement('span');
      s.className = 'ch';
      s.setAttribute('aria-hidden', 'true');
      s.textContent = c;
      typeH1.appendChild(s);
      return s;
    });
    const cursor = document.createElement('span');
    cursor.className = 'type-cursor';
    cursor.setAttribute('aria-hidden', 'true');
    typeH1.classList.add('ready');
    let i = 0;
    const step = Math.max(18, Math.min(45, 1400 / chars.length));
    const tick = () => {
      chars[i].classList.add('on');
      chars[i].after(cursor);
      i += 1;
      if (i < chars.length) setTimeout(tick, chars[i - 1].textContent === ' ' ? step * 0.6 : step);
      else cursor.classList.add('bitti');
    };
    setTimeout(tick, 250);
  }
}
