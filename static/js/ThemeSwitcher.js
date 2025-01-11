// const updateHeroBannerBackground = (theme) => {
//   const darkThemeImage = "static/img/lucerne.jpg";
//   if (document.getElementById('hero-banner')) {
//     if (theme === 'dark') {
//       console.log("Setting background...")
//       heroBanner.style.backgroundImage = `url('${darkThemeImage}')`;
//     }
//   }
// };

// URLs for logos
const lightLogo = '{% static "/logo/prokope-light.png" %}';
const darkLogo = '{% static "/logo/prokope-dark.png" %}';
const updateLogo = (theme) => {
  if (brandLogo) {
    const lightLogo = brandLogo.getAttribute('data-light-logo');
    const darkLogo = brandLogo.getAttribute('data-dark-logo');
    brandLogo.src = theme === 'dark' ? darkLogo : lightLogo;
  }
};

const body = document.documentElement;
const toggleButton = document.getElementById('darkModeToggle');
const icon = document.getElementById('darkModeIcon');
let isManualToggle = false; // Tracks whether the user manually toggled the theme

// Function to set the theme and update the UI
const setTheme = (theme, savePreference = false) => {
    updateLogo(theme);
    body.setAttribute('data-theme', theme);
    icon.className = theme === 'dark' ? 'fa fa-sun-o' : 'fa fa-moon-o';
    if (savePreference) {
        localStorage.setItem('theme', theme);
        isManualToggle = true; // Record that the user manually toggled the theme
    }
};

// Detect user's system preference
const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

// Determine the initial theme
const getInitialTheme = () => {
    const storedTheme = localStorage.getItem('theme');
    // updateHeroBannerBackground(storedTheme);
    if (storedTheme) {
        return storedTheme; // User manually selected a theme
    } else if (prefersDarkScheme.matches) {
        return 'dark'; // System preference is dark
    }
    else {
        return 'light'; // System preference is light
    }
};

// Apply the initial theme
const initialTheme = getInitialTheme();
setTheme(initialTheme);

// Manual theme toggle
toggleButton.addEventListener('click', () => {
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme, true); // Save preference on manual toggle
});

// Listen for system theme changes
prefersDarkScheme.addEventListener('change', (event) => {
    if (!isManualToggle) { // Only apply system changes if the user hasn't toggled manually
        const systemTheme = event.matches ? 'dark' : 'light';
        setTheme(systemTheme);
        // updateHeroBannerBackground(systemTheme);
    }
});