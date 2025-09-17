// Header shrink on scroll
const header = document.querySelector('.site-header');
let lastY = window.scrollY;
window.addEventListener('scroll', () => {
  const y = window.scrollY;
  if (y > 10) header.classList.add('shrink'); else header.classList.remove('shrink');
  lastY = y;
});

// Scroll reveal animations
const revealEls = document.querySelectorAll('[data-reveal]');
const observer = new IntersectionObserver((entries) => {
  for (const entry of entries) {
    if (entry.isIntersecting) {
      entry.target.classList.add('revealed');
      observer.unobserve(entry.target);
    }
  }
}, { threshold: 0.15 });
revealEls.forEach(el => observer.observe(el));

// Active nav highlight
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav a[href^="#"]');
const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.getAttribute('id');
      navLinks.forEach(l => l.classList.toggle('active', l.getAttribute('href') === `#${id}`));
    }
  });
}, { rootMargin: '-40% 0px -50% 0px', threshold: 0 });
sections.forEach(s => sectionObserver.observe(s));

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (!target) return;
    e.preventDefault();
    target.scrollIntoView({ behavior: 'smooth' });
  });
});

// Auto-hide toasts
document.querySelectorAll('.toast').forEach(t => {
  setTimeout(() => { t.classList.add('hide'); }, 3000);
  t.addEventListener('click', () => t.classList.add('hide'));
});

// Wave animation
const wave = document.querySelector('.wave');
if (wave) {
  setInterval(() => {
    wave.style.transform = 'rotate(0deg)';
    setTimeout(() => wave.style.transform = 'rotate(20deg)', 100);
    setTimeout(() => wave.style.transform = 'rotate(-10deg)', 200);
    setTimeout(() => wave.style.transform = 'rotate(0deg)', 300);
  }, 3000);
}

// Floating elements animation delay
document.querySelectorAll('.float-element').forEach((el, i) => {
  el.style.animationDelay = `${i * 2}s`;
});


