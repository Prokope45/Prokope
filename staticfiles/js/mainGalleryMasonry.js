import { observeLazyElements } from './lazyLoader/lazyLoader.js';

document.addEventListener('DOMContentLoaded', function() {
  const select = document.getElementById('city-filter');
  const form = document.querySelector("#city-selector-form");
  var elem = document.querySelector('#masonry-container');
  let msnry;

  // Function to initialize Masonry after images are loaded
  function initializeMasonry() {
    // Destroy existing Masonry instance if it exists
    if (msnry) {
      msnry.destroy();
    }

    msnry = new Masonry( elem, {
      itemSelector: '.gallery_product:not(.hidden)',
      columnWidth: '.gallery_product',
      isFitWidth: true
    });
     // Layout after Masonry is initialized
    msnry.layout();
  }

  imagesLoaded(elem).on('always', function() {
    initializeMasonry();
    observeLazyElements(msnry);
  });

  form.addEventListener('submit', function(event) {
    // Prevent form submission.
    // event.preventDefault();
    const value = select.value;

    document.querySelectorAll('.gallery_product').forEach(item => {
      if (value === 'all') {
        $(item).fadeIn(300);
        $(item).show(300);
        $(item).removeClass('hidden');
      } else if (item.classList.contains(value)) {
        $(item).fadeIn(500);
        $(item).show(500);
        $(item).removeClass('hidden');
      } else {
        $(item).fadeOut(500);
        $(item).hide(500);
        $(item).addClass('hidden');
      }
      msnry.reloadItems();
    });
    msnry.layout();
  });

  // Trigger form submission once animation is finished.
  select.addEventListener('change', function() {
    form.dispatchEvent(new Event('submit'));
  });
});
