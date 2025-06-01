// Blog post image lightbox effect
document.addEventListener('DOMContentLoaded', function() {
    // Automatically wrap all images in links for lightbox
    const images = document.querySelectorAll('.card-body img');
    images.forEach(image => {
        const imageUrl = image.src;
        const lightboxLink = document.createElement('a');
        lightboxLink.href = imageUrl;
        lightboxLink.setAttribute('data-lightbox', 'article-images');
        lightboxLink.style.display = 'inline-block';
        image.parentNode.insertBefore(lightboxLink, image);
        lightboxLink.appendChild(image);
    });
});