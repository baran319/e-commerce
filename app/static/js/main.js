/* ================================================================
   FitMarket — Main JS (flash dismiss + header scroll shadow)
   ================================================================ */

// Header scroll shadow
window.addEventListener('scroll', () => {
  const header = document.querySelector('.main-header');
  if (header) {
    header.style.boxShadow = window.scrollY > 10
      ? '0 2px 12px rgba(0,0,0,0.15)'
      : 'none';
  }
});

// Auto-dismiss flash messages after 4.5 seconds
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.flash').forEach(flash => {
    setTimeout(() => {
      flash.style.opacity = '0';
      flash.style.transition = 'opacity 0.4s ease';
      setTimeout(() => flash.remove(), 400);
    }, 4500);
  });
});
