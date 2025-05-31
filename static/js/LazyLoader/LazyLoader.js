document.addEventListener("DOMContentLoaded", () => {
  const lazyElements = document.querySelectorAll('[data-lazy]');

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;

      const el = entry.target;
      const type = el.dataset.lazy;

      if (type === 'image') {
        const spinner = el.closest('[data-masonry-item]')?.querySelector('.spinner');
        el.src = el.dataset.src;
        el.onload = () => {
          el.style.opacity = 1;
          spinner?.remove();
          // If using Masonry
          if (window.masonry) window.masonry.layout();
        };
      }

      if (type === 'section') {
        const delay = el.getAttribute('data-delay');
        if (delay) {
          el.style.transitionDelay = `${delay}ms`;
        }

        const duration = el.getAttribute('data-duration');
        if (duration) {
          el.style.transitionDuration = `${duration}ms`;
        }

        el.classList.add('in-view');
      }

      obs.unobserve(el);
    });
  });

  lazyElements.forEach(el => observer.observe(el));
});