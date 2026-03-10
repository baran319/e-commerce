/* ================================================================
   FitMarket — Main JS
   Global interactions: navbar scroll, flash dismiss, etc.
   ================================================================ */

// Navbar scroll shadow
window.addEventListener('scroll', () => {
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    navbar.style.boxShadow = window.scrollY > 20
      ? '0 4px 32px rgba(0,0,0,0.5)'
      : 'none';
  }
});

// Auto-dismiss flash messages after 4 seconds
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.flash').forEach(flash => {
    setTimeout(() => {
      flash.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      flash.style.opacity = '0';
      flash.style.transform = 'translateY(-8px)';
      setTimeout(() => flash.remove(), 500);
    }, 4000);
  });
});

// Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const iconLight = document.querySelector('.theme-icon-light');
  const iconDark = document.querySelector('.theme-icon-dark');

  if (!themeToggleBtn) return;

  function updateIcons(isDark) {
    if (isDark) {
      iconLight.style.display = 'inline-block';
      iconDark.style.display = 'none';
    } else {
      iconLight.style.display = 'none';
      iconDark.style.display = 'inline-block';
    }
  }

  // Initialize icon upon load
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  updateIcons(isDark);

  themeToggleBtn.addEventListener('click', () => {
    let currentTheme = document.documentElement.getAttribute('data-theme');
    let targetTheme = currentTheme === 'dark' ? 'light' : 'dark';

    document.documentElement.setAttribute('data-theme', targetTheme);
    localStorage.setItem('theme', targetTheme);
    updateIcons(targetTheme === 'dark');
  });
});
