var ready = (callback) => {
    if (document.readyState != "loading") callback();
    else document.addEventListener("DOMContentLoaded", callback);
}
ready(() => {
    document.querySelector(".header").style.height = window.innerHeight + "px";
})

const body = document.body;
const toggleButton = document.getElementById('darkModeToggle');
const icon = document.getElementById('darkModeIcon');
let isManualToggle = false; // Tracks whether the user manually toggled the theme

// Function to set the theme and update the UI
const setTheme = (theme, savePreference = false) => {
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
    if (storedTheme) {
    console.log("Using stored theme:", storedTheme);
    return storedTheme; // User manually selected a theme
    } else if (prefersDarkScheme.matches) {
    console.log("Using system preference: Dark");
    return 'dark'; // System preference is dark
    } else {
    console.log("Using system preference: Light");
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
    console.log("Toggled Theme Manually:", newTheme);
    setTheme(newTheme, true); // Save preference on manual toggle
});

// Listen for system theme changes
prefersDarkScheme.addEventListener('change', (event) => {
    if (!isManualToggle) { // Only apply system changes if the user hasn't toggled manually
        const systemTheme = event.matches ? 'dark' : 'light';
        console.log("System Theme Change Detected:", systemTheme);
        setTheme(systemTheme);
    }
});
