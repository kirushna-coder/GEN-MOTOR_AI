// ── GenMentor AI — Main JS ──────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  const sidebar  = document.getElementById('sidebar');
  const hamburger = document.getElementById('hamburger');
  const main     = document.getElementById('main-content');

  // Toggle sidebar on mobile
  if (hamburger) {
    hamburger.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });
  }

  // Close sidebar when clicking main content on mobile
  if (main) {
    main.addEventListener('click', () => {
      if (sidebar.classList.contains('open')) {
        sidebar.classList.remove('open');
      }
    });
  }

  // Animate elements on scroll
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in-visible');
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.glass-card, .feature-card, .stat-card, .quick-card').forEach(el => {
    el.classList.add('fade-in');
    observer.observe(el);
  });

  // Drop zone interactions
  const dropZone = document.getElementById('dropZone');
  if (dropZone) {
    ['dragover','dragenter'].forEach(e => {
      dropZone.addEventListener(e, (ev) => {
        ev.preventDefault();
        dropZone.style.borderColor = '#8B5CF6';
      });
    });
    ['dragleave','drop'].forEach(e => {
      dropZone.addEventListener(e, () => {
        dropZone.style.borderColor = '';
      });
    });
  }
});

// ── Fade-in animation ──────────────────────────────────
const style = document.createElement('style');
style.textContent = `
  .fade-in {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }
  .fade-in-visible {
    opacity: 1;
    transform: translateY(0);
  }
`;
document.head.appendChild(style);
