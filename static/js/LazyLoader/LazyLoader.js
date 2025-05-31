document.addEventListener("DOMContentLoaded", () => {
  const lazyElements = document.querySelectorAll('[data-lazy]');
  var elem = document.querySelector('#masonry-container');
  let msnry;

  // Function to initialize Masonry after images are loaded
  function initializeMasonry() {
    // Destroy existing Masonry instance if it exists
    if (msnry) {
      msnry.destroy();
    }

    msnry = new Masonry( elem, {
      itemSelector: '.gallery_product',
      columnWidth: '.gallery_product',
      isFitWidth: true
    });
     // Layout after Masonry is initialized
    msnry.layout();
  }

  // Load images first
  imagesLoaded(elem).on('always', function() {
    initializeMasonry();
  });

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;

      const el = entry.target;
      const type = el.dataset.lazy;

      if (type === 'image') {
        const spinner = el.closest('[data-masonry-item]')?.querySelector('.spinner');
        el.src = el.dataset.src;
        el.onload = () => {
          el.classList.add('in-view');
          spinner?.remove();
          // If using Masonry
          // if (window.masonry) window.masonry.layout();
          msnry.layout();
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