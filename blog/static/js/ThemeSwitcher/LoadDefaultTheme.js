(() => {
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    const storedTheme = localStorage.getItem('theme');
    const theme = storedTheme || (prefersDarkScheme.matches ? "dark" : "light");
    document.documentElement.setAttribute("data-theme", theme);
})();