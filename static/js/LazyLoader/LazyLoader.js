export function observeLazyElements(msnry = null) {
  const lazyElements = document.querySelectorAll('[data-lazy]');
  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;

      const el = entry.target;
      const type = el.dataset.lazy;

      if (type === 'image') {
        const spinner = el.closest('[data-masonry-item]')?.querySelector('.spinner');
        const src = el.getAttribute('data-src');
        
        if (src) {
          el.src = src;
          el.onload = () => {
            el.classList.add('in-view');
            spinner?.remove();
            if (msnry != null) msnry.layout();
          };
          el.classList.remove('lazy-image');
        }
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
}