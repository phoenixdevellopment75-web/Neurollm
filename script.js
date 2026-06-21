/**
 * Project SparseMind - Minimal UI Theme Switcher
 */

const themeToggleBtn = document.getElementById('themeToggleBtn');
const themeIcon = document.getElementById('themeIcon');

function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
        if (themeIcon) themeIcon.textContent = 'light_mode';
    } else {
        document.body.classList.remove('light-theme');
        if (themeIcon) themeIcon.textContent = 'dark_mode';
    }
}

if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
        document.body.classList.toggle('light-theme');
        const isLight = document.body.classList.contains('light-theme');
        
        if (themeIcon) {
            themeIcon.textContent = isLight ? 'light_mode' : 'dark_mode';
        }
        localStorage.setItem('theme', isLight ? 'light' : 'dark');
    });
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
    initTheme();
});
