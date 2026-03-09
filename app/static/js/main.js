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
