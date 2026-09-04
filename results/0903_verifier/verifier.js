const root = document.documentElement;
document.getElementById('t').onclick = () =>
  root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
const btns = [...document.querySelectorAll('[data-f]')];
btns.forEach(b => b.onclick = () => {
  btns.forEach(x => x.setAttribute('aria-pressed', x === b));
  const f = b.dataset.f;
  document.querySelectorAll('.card').forEach(c =>
    c.classList.toggle('hide', f !== 'all' && !c.dataset.tags.split(' ').includes(f)));
  document.querySelectorAll('.g').forEach(h => {
    let n = h.nextElementSibling, any = false;
    while (n && n.classList.contains('card')) { any ||= !n.classList.contains('hide'); n = n.nextElementSibling; }
    h.classList.toggle('hide', !any);
  });
});
