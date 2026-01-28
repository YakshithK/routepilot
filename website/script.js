// Lightweight progressive enhancement for the static landing page.
// No dependencies. Safe to remove if you want pure HTML/CSS.

(function () {
  // Update active nav link based on scroll position.
  const links = Array.from(document.querySelectorAll('.nav-link'));
  const sections = links
    .map((a) => {
      const id = a.getAttribute('href');
      if (!id || !id.startsWith('#')) return null;
      const el = document.querySelector(id);
      return el ? { a, el } : null;
    })
    .filter(Boolean);

  if (!sections.length) return;

  const onScroll = () => {
    const y = window.scrollY + 120;
    let current = sections[0];
    for (const s of sections) {
      if (s.el.offsetTop <= y) current = s;
    }
    for (const s of sections) s.a.removeAttribute('aria-current');
    current.a.setAttribute('aria-current', 'page');
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();


