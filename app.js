const io = new IntersectionObserver((entries)=>{
  entries.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('show'); io.unobserve(e.target);} });
},{threshold:.15});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

const MARQUEE_SPEED = 70;
const startMarquee = (track) => {
  const distance = track.scrollWidth / 2;
  if (distance > 0) {
    track.style.setProperty('--marquee-duration', `${Math.max(distance / MARQUEE_SPEED, 12)}s`);
    track.classList.add('is-ready');
  }
};
// Kart boyutları sabit olduğu için görsellerin yüklenmesini beklemeye gerek yok
document.querySelectorAll('.marquee .track').forEach(startMarquee);
window.addEventListener('resize', () => document.querySelectorAll('.marquee .track').forEach(startMarquee));

const toggle = document.querySelector('.nav-toggle');
const menu = document.querySelector('#site-menu');

if (toggle && menu) {
  const setOpen = (open) => {
    menu.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Menüyü kapat' : 'Menüyü aç');
  };

  toggle.addEventListener('click', () => {
    setOpen(!menu.classList.contains('open'));
  });

  menu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => setOpen(false));
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') setOpen(false);
  });
}
