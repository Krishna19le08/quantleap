(() => {
  'use strict';

  // load html components (<div data-include="components/x.html">), nested ones included
  const include = async root => {
    const slots = [...root.querySelectorAll('[data-include]')];
    await Promise.all(slots.map(async slot => {
      const res = await fetch(slot.dataset.include);
      if (!res.ok) throw new Error(`Failed to load ${slot.dataset.include}`);
      const tpl = document.createElement('template');
      tpl.innerHTML = await res.text();
      await include(tpl.content);
      slot.replaceWith(tpl.content);
    }));
  };

  const init = () => {

  // #top points at the header, which is position:fixed once scrolled, so the browser would not move; scroll to 0 ourselves
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href="#top"]');
    if (!a) return;
    e.preventDefault();
    window.scrollTo({ top: 0 });          // honours html{scroll-behavior} (smooth, or auto for reduced motion)
    history.replaceState(null, '', '#top');
  });

  // sticky header
  const header = document.querySelector('.site-header');
  const onScroll = () => header.classList.toggle('stuck', window.scrollY > 60);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // mobile menu
  const burger = document.getElementById('burger');
  const nav = document.getElementById('nav');
  const backdrop = document.getElementById('nav-backdrop');
  const compact = matchMedia('(max-width:1000px)');
  const subToggle = nav.querySelector('.has-sub > a');
  const setSub = open => {
    subToggle.parentElement.classList.toggle('open', open);
    if (compact.matches) subToggle.setAttribute('aria-expanded', open); else subToggle.removeAttribute('aria-expanded');
  };
  const setMenu = open => {
    nav.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', open);
    document.documentElement.classList.toggle('menu-open', open);
    document.body.classList.toggle('menu-open', open);
    if (!open) setSub(false);
  };
  // desktop: dropdown is hover/focus driven; compact: tapping the parent link expands it as an accordion
  subToggle.setAttribute('aria-haspopup', 'true');
  setSub(false);
  subToggle.addEventListener('click', e => {
    if (!compact.matches) return;
    e.preventDefault();
    setSub(!subToggle.parentElement.classList.contains('open'));
  });
  compact.addEventListener('change', () => { setMenu(false); });
  burger.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
  if (backdrop) {
    backdrop.addEventListener('click', () => setMenu(false));
    backdrop.addEventListener('touchmove', e => {
      if (nav.classList.contains('open')) e.preventDefault();
    }, { passive: false });
  }
  document.addEventListener('click', e => {
    if (nav.classList.contains('open') && !nav.contains(e.target) && !burger.contains(e.target)) {
      setMenu(false);
    }
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); burger.focus(); }
  });
  nav.addEventListener('click', e => {
    const a = e.target.closest('a');
    if (a && !(a === subToggle && compact.matches)) setMenu(false);
  });

  // active nav link on scroll: last section whose top is above 40% of the viewport; Home at the top
  const links = [...nav.querySelectorAll('a[href^="#"]')];
  const target = a => { const h = a.getAttribute('href'); return h === '#top' ? document.querySelector('.hero') : document.querySelector(h); };
  const spied = links.map(a => ({ a, s: target(a) })).filter(x => x.s);
  const spy = () => {
    const y = window.scrollY + window.innerHeight * .4;
    let cur = spied[0].s;
    spied.forEach(({ s }) => { if (s.offsetTop <= y && s.offsetTop >= cur.offsetTop) cur = s; });
    spied.forEach(({ a, s }) => a.classList.toggle('active', s === cur));
  };
  spy();
  window.addEventListener('scroll', spy, { passive: true });
  window.addEventListener('resize', spy);

  // carousel: arrows page the track one card at a time
  const car = document.getElementById('carousel');
  const arrows = document.querySelectorAll('.car-btn');
  arrows.forEach(b =>
    b.addEventListener('click', () => {
      const card = car.querySelector('.vcard');
      car.scrollBy({ left: +b.dataset.dir * (card.offsetWidth + 16), behavior: 'smooth' });
    }));
  // arrows are disabled (not removed) when there is nothing further to scroll to in that direction
  const syncArrows = () => {
    const max = car.scrollWidth - car.clientWidth;
    arrows.forEach(b => { b.disabled = +b.dataset.dir < 0 ? car.scrollLeft <= 1 : car.scrollLeft >= max - 1; });
  };
  syncArrows();
  car.addEventListener('scroll', syncArrows, { passive: true });
  window.addEventListener('resize', syncArrows);
  window.addEventListener('load', syncArrows);

  // reveal on scroll
  const targets = document.querySelectorAll('.pillar,.vcard,.icard,.steps li,.nation-list li,.locs li,.section-light h2,.section-dark h2');
  targets.forEach(t => t.classList.add('reveal'));
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { threshold: .12 });
  targets.forEach((t, i) => { t.style.transitionDelay = (i % 5) * 70 + 'ms'; io.observe(t); });

  // our impact: staggered entrance + count-up, replayed every time the section scrolls into view
  const impact = document.querySelector('.impact');
  if (impact && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const nums = [...impact.querySelectorAll('[data-count]')];
    const frames = new Map();
    const show = (el, v) => { el.textContent = (el.dataset.prefix || '') + v + (el.dataset.suffix || ''); };
    const count = el => {
      const end = +el.dataset.count, t0 = performance.now() + 450, dur = 1600;
      const tick = t => {
        const p = Math.min(Math.max((t - t0) / dur, 0), 1);
        show(el, Math.round(end * (1 - Math.pow(1 - p, 3))));
        if (p < 1) frames.set(el, requestAnimationFrame(tick));
      };
      frames.set(el, requestAnimationFrame(tick));
    };
    const reset = () => nums.forEach(el => { cancelAnimationFrame(frames.get(el)); show(el, 0); });
    impact.querySelectorAll('.eyebrow,h2,.stats li').forEach((el, i) => el.style.setProperty('--d', i < 2 ? i * 120 : 260 + (i - 2) * 140));
    impact.classList.add('anim');
    reset();
    new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { impact.classList.add('in'); nums.forEach(count); }
      else { impact.classList.remove('in'); reset(); }
    }), { threshold: .35 }).observe(impact);
  }

  // modals: any [data-modal="id"] opens #id; focus is trapped inside and returned to the opener
  let openModal = null, opener = null;
  const focusables = m => [...m.querySelectorAll('a[href],button:not([disabled]),[tabindex]:not([tabindex="-1"])')];
  const showModal = (m, from) => {
    openModal = m; opener = from; m.hidden = false;
    document.documentElement.classList.add('modal-open');
    const id = m.dataset.video;   // video modals build their iframe on open and drop it on close, so playback stops
    if (id) {
      const f = document.createElement('iframe');
      f.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0&playsinline=1`;
      f.title = 'QuantLeap story video';
      f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      f.allowFullscreen = true;
      m.querySelector('.video-frame').replaceChildren(f);
    }
    m.querySelector('.modal-close').focus();
  };
  const clearVideo = m => { const v = m.querySelector('.video-frame'); if (v) v.replaceChildren(); };
  const closeModal = () => {
    if (!openModal) return;
    openModal.hidden = true; clearVideo(openModal); openModal = null;
    document.documentElement.classList.remove('modal-open');
    if (opener) opener.focus();
    opener = null;
  };
  // the modal markup is fetched on the first click, not at page load
  let modalsReady = null;
  const loadModals = () => modalsReady ||= (async () => {
    const host = document.createElement('div');
    host.dataset.include = 'components/modal.html';
    document.body.append(host);
    await include(document.body);
    document.querySelectorAll('.modal').forEach(m => m.addEventListener('click', e => {
      if (e.target === m || e.target.closest('.modal-close')) closeModal();
      else if (e.target.closest('a[href^="#"]')) { openModal.hidden = true; clearVideo(openModal); openModal = null; opener = null; document.documentElement.classList.remove('modal-open'); }
    }));
  })().catch(err => { modalsReady = null; throw err; });
  document.addEventListener('click', async e => {
    const a = e.target.closest('[data-modal]');
    if (!a) return;
    e.preventDefault();
    await loadModals();
    const m = document.getElementById(a.dataset.modal);
    if (m) showModal(m, a);
  });
  document.addEventListener('keydown', e => {
    if (!openModal) return;
    if (e.key === 'Escape') { closeModal(); return; }
    if (e.key !== 'Tab') return;
    const f = focusables(openModal);
    const first = f[0], last = f[f.length - 1];
    if (!openModal.contains(document.activeElement)) { e.preventDefault(); first.focus(); }
    else if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });
  };

  // block right-click, view-source and devtools shortcuts (F12, Ctrl+Shift+I/J/C, Ctrl+U)
  document.addEventListener('contextmenu', e => e.preventDefault());
  document.addEventListener('keydown', e => {
    const k = e.key.toLowerCase();
    if (e.key === 'F12' || (e.ctrlKey || e.metaKey) && (k === 'u' || e.shiftKey && 'ijc'.includes(k)) || e.metaKey && e.altKey && 'iju'.includes(k)) e.preventDefault();
  });

  include(document).then(init).catch(err => console.error(err));
})();
