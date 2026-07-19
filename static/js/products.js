/**
 * NovaGear — Product catalog data
 * Replace with Django API / template context later
 */

// Simple product page scripts
    let currentQty = 1;

    function changeQty(delta) {
      currentQty = Math.max(1, currentQty + delta);
      document.getElementById('qty-value').textContent = currentQty;
    }

    function addToCart() {
      const toast = document.querySelector('[data-toast]');
      const toastMsg = document.querySelector('[data-toast-message]');
      toastMsg.textContent = 'ProMouse X1 added to cart!';
      toast.classList.add('is-visible');
      toast.removeAttribute('hidden');

      setTimeout(() => {
        toast.classList.remove('is-visible');
        setTimeout(() => toast.setAttribute('hidden', ''), 400);
      }, 2800);
    }

    function toggleWishlist(btn) {
      if (btn.classList.contains('is-active')) {
        btn.innerHTML = `<span style="font-size: 1.2em;">♡</span> Add to Wishlist`;
        btn.classList.remove('is-active');
      } else {
        btn.innerHTML = `<span style="font-size: 1.2em;">♥</span> In Wishlist`;
        btn.classList.add('is-active');
      }
    }

    function switchTab(n) {
      document.querySelectorAll('.tabs__btn').forEach((b, i) => {
        b.classList.toggle('tabs__btn--active', i === n);
      });
      document.querySelectorAll('.tab-content').forEach((c, i) => {
        c.style.display = i === n ? 'block' : 'none';
      });
    }

    // Thumbnail click
    document.querySelectorAll('.product-thumbnail').forEach(thumb => {
      thumb.addEventListener('click', () => {
        document.querySelectorAll('.product-thumbnail').forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');

        const newSrc = thumb.getAttribute('data-img');
        document.getElementById('main-img').src = newSrc;
      });
    });

    // Initialize
    window.addEventListener('load', () => {
      // You can load related products here from products.js if available
    });

document.addEventListener('DOMContentLoaded', function() {
    initTabs();
});

function initTabs() {
    const tabsContainer = document.querySelector('[data-tabs]');
    if (!tabsContainer) return;

    const tabButtons = tabsContainer.querySelectorAll('[data-tab]');
    const tabContents = document.querySelectorAll('[data-tab-content]');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');

            // Убираем активный класс у всех кнопок
            tabButtons.forEach(btn => btn.classList.remove('tabs__btn--active'));
            // Добавляем активный класс текущей кнопке
            this.classList.add('tabs__btn--active');

            // Скрываем все табы
            tabContents.forEach(content => content.classList.add('hidden'));
            // Показываем нужный таб
            const targetContent = document.getElementById('tab-' + targetTab);
            if (targetContent) {
                targetContent.classList.remove('hidden');
            }
        });
    });
}