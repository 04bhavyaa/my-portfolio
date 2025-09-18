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

// Theme Toggle Functionality
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');
const themeText = document.getElementById('theme-text');
const body = document.body;

// Check for saved theme preference or default to dark theme
const currentTheme = localStorage.getItem('theme') || 'dark';
body.setAttribute('data-theme', currentTheme);
updateThemeUI(currentTheme);

function updateThemeUI(theme) {
  if (theme === 'light') {
    themeIcon.innerHTML = `
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
    `;
    themeText.textContent = 'Dark';
  } else {
    themeIcon.innerHTML = `
      <circle cx="12" cy="12" r="5"></circle>
      <line x1="12" y1="1" x2="12" y2="3"></line>
      <line x1="12" y1="21" x2="12" y2="23"></line>
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
      <line x1="1" y1="12" x2="3" y2="12"></line>
      <line x1="21" y1="12" x2="23" y2="12"></line>
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
    `;
    themeText.textContent = 'Light';
  }
}

themeToggle.addEventListener('click', () => {
  const currentTheme = body.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  
  body.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  updateThemeUI(newTheme);
});

// Projects: Filter by role and sort by date
(() => {
  const grid = document.getElementById('projects-grid');
  if (!grid) return;
  const cards = Array.from(grid.querySelectorAll('.project-card'));
  const roleChips = document.querySelectorAll('#role-filter .chip');
  const sortSelect = document.getElementById('project-sort');

  let activeRole = 'all';
  let sortOrder = sortSelect ? sortSelect.value : 'desc';

  function parseYear(str) {
    if (!str) return 0;
    const m = String(str).match(/(20\d{2}|19\d{2})/);
    return m ? parseInt(m[1], 10) : 0;
  }

  function apply() {
    // Filter
    cards.forEach((card) => {
      const role = (card.getAttribute('data-role') || '').toLowerCase();
      const show = activeRole === 'all' || role === activeRole;
      card.style.display = show ? '' : 'none';
    });
    // Sort
    const visible = cards.filter((c) => c.style.display !== 'none');
    visible.sort((a, b) => {
      const ay = parseYear(a.getAttribute('data-date'));
      const by = parseYear(b.getAttribute('data-date'));
      return sortOrder === 'asc' ? ay - by : by - ay;
    });
    visible.forEach((el) => grid.appendChild(el));
  }

  roleChips.forEach((chip) => {
    chip.addEventListener('click', () => {
      roleChips.forEach((c) => c.classList.remove('active'));
      chip.classList.add('active');
      activeRole = chip.getAttribute('data-role');
      apply();
    });
  });

  if (sortSelect) {
    sortSelect.addEventListener('change', () => {
      sortOrder = sortSelect.value;
      apply();
    });
  }

  // Init
  const allChip = document.querySelector('#role-filter .chip[data-role="all"]');
  if (allChip) allChip.classList.add('active');
  apply();
})();

// Request Phone / CV: autofill contact form and scroll
(() => {
  const buttons = document.querySelectorAll('.request-btn');
  if (!buttons.length) return;
  const form = document.querySelector('#contact form.contact-form');
  const message = form ? form.querySelector('textarea[name="message"]') : null;
  const emailInput = form ? form.querySelector('input[name="email"]') : null;

  function makeBody(kind) {
    if (kind === 'phone') {
      return 'Hello, I would like to request your phone number to discuss an opportunity.\n\nReason: ';
    }
    return 'Hello, I would like to request your latest CV.\n\nReason: ';
  }

  buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
      if (!form || !message) return;
      const kind = btn.getAttribute('data-request');
      message.value = makeBody(kind);
      form.scrollIntoView({ behavior: 'smooth' });
      const nameInput = form.querySelector('input[name="name"]');
      if (nameInput) nameInput.focus();
    });
  });

  if (emailInput) {
    emailInput.addEventListener('input', () => {
      if (emailInput.validity.typeMismatch) {
        emailInput.setCustomValidity('Please enter a valid email address');
      } else {
        emailInput.setCustomValidity('');
      }
    });
  }
})();


