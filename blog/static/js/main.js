var ready = (callback) => {
    if (document.readyState != "loading") callback();
    else document.addEventListener("DOMContentLoaded", callback);
}
ready(() => {
    document.querySelector(".header").style.height = window.innerHeight + "px";
})

// const updateHeroBannerBackground = (theme) => {
//   const darkThemeImage = "static/img/lucerne.jpg";
//   if (document.getElementById('hero-banner')) {
//     if (theme === 'dark') {
//       console.log("Setting background...")
//       heroBanner.style.backgroundImage = `url('${darkThemeImage}')`;
//     }
//   }
// };

const brandLogo = document.getElementById('brand-logo')

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

const body = document.body;
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
    } else {
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

function setupTypewriter(t) {
    try {

        var HTML = t.innerHTML;
    
        t.innerHTML = "";
    
        var cursorPosition = 0,
            tag = "",
            writingTag = false,
            tagOpen = false,
            typeSpeed = 100,
            tempTypeSpeed = 0;
    
        var type = function() {
            // Skip the img block
            if (HTML.slice(cursorPosition, cursorPosition + 4) === "<img") {
                // Extract the <img> tag
                let imgTag = "";
                while (HTML[cursorPosition] !== ">" && cursorPosition < HTML.length) {
                    imgTag += HTML[cursorPosition];
                    cursorPosition++;
                }
                imgTag += ">"; // Include the closing ">"
    
                // Append the <img> element to the DOM
                const div = document.createElement("div");
                div.innerHTML = imgTag;
                t.appendChild(div.firstChild);
    
                cursorPosition++; // Move past the closing ">"
                return type(); // Restart the typing loop
            }
            
            if (writingTag === true) {
                tag += HTML[cursorPosition];
            }
    
            if (HTML[cursorPosition] === "<") {
                tempTypeSpeed = 0;
                if (tagOpen) {
                    tagOpen = false;
                    writingTag = true;
                } else {
                    tag = "";
                    tagOpen = true;
                    writingTag = true;
                    tag += HTML[cursorPosition];
                }
            }
            if (!writingTag && tagOpen) {
                tag.innerHTML += HTML[cursorPosition];
            }
            if (!writingTag && !tagOpen) {
                if (HTML[cursorPosition] === " ") {
                    tempTypeSpeed = 0;
                }
                else {
                    tempTypeSpeed = (Math.random() * typeSpeed) + 50;
                }
                t.innerHTML += HTML[cursorPosition];
            }
            if (writingTag === true && HTML[cursorPosition] === ">") {
                tempTypeSpeed = (Math.random() * typeSpeed) + 50;
                writingTag = false;
                if (tagOpen) {
                    var newSpan = document.createElement("span");
                    t.appendChild(newSpan);
                    newSpan.innerHTML = tag;
                    tag = newSpan.firstChild;
                }
            }
    
            cursorPosition += 1;
            if (cursorPosition < HTML.length - 1) {
                setTimeout(type, tempTypeSpeed);
            }
        };
    
        return {
            type: type
        };
    } catch (error) {
        console.error(error);
    }
}

var typer = document.getElementById('typewriter');

typewriter = setupTypewriter(typer);

typewriter.type();