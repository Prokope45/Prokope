import { observeLazyElements } from '../lazyLoader/lazyLoader.js';

document.addEventListener("DOMContentLoaded", () => {
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

  // File is imported globally for all apps.
  if (elem != null) {
    // Masonry is first initialized then lazily load images. 
    imagesLoaded(elem).on('always', function() {
      initializeMasonry();
      observeLazyElements(msnry);
    });
  } else {
    // Otherwise, lazily load images.
    observeLazyElements();
  }
});