// Mobil menü
const btn = document.querySelector('.menu-btn');
const nav = document.querySelector('.site-header nav');

if (btn && nav) {
  const setOpen = (open) => {
    nav.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', String(open));
    btn.textContent = open ? 'Kapat' : 'Menü';
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
      say(first.type === 'checkbox'
        ? 'Göndermek için KVKK aydınlatma metnini onaylayın.'
        : 'Lütfen işaretli alanları doldurun.', 'err');
      first.focus();
      return;
    }
    if (mail.value && !mail.checkValidity()) {
      mail.setAttribute('aria-invalid', 'true');
      say('E-posta adresini kontrol edin.', 'err');
      mail.focus();
      return;
    }

    const data = Object.fromEntries(new FormData(form));
    delete data.redirect;
    submit.disabled = true;
    say('Gönderiliyor…');
    try {
      const res = await fetch(form.action, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(data),
      });
      const out = await res.json();
      if (!res.ok || !out.success) throw new Error(out.message || res.status);
      form.reset();
      say('Talebiniz bize ulaştı. Mesai saatlerinde size dönüş yapacağız.', 'ok');
    } catch (err) {
      say('Gönderilemedi. Lütfen tekrar deneyin ya da 0532 586 18 60 numarasından bize ulaşın.', 'err');
    } finally {
      submit.disabled = false;
    }
  });
}
