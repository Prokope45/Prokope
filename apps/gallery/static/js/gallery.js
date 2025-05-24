document.addEventListener('DOMContentLoaded', function() {
  const select = document.getElementById('city-filter');
  const form = document.querySelector('form');

  form.addEventListener('submit', function(event) {
    // Prevent form submission.
    event.preventDefault();
    const value = select.value;

    if (value.toLowerCase() === 'all') {
      $('.filter').show('3000');
    } else {
      // Hide photos not related to selected city.
      $(".filter").not('.'+value).hide('7000');
      // Show photos not related to selected city.
      $('.filter').filter('.'+value).show('7000');
    }
  });

  // Trigger form submission once animation is finished.
  select.addEventListener('change', function() {
    form.dispatchEvent(new Event('submit'));
  });
});
