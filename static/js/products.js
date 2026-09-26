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

    async function toggleWishlist(btn) {
        const url = btn.dataset.wishlistUrl;

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }

            const data = await response.json();

            updateWishlistButton(btn, data.is_in_wishlist);

        } catch (error) {
            console.error('Wishlist error:', error);
        }
    }


    function updateWishlistButton(btn, isInWishlist) {

        btn.classList.toggle('is-active', isInWishlist);

        // Страница товара
        if (btn.classList.contains('product-wishlist-btn')) {

            btn.innerHTML = isInWishlist
                ? `<span style="font-size: 1.2em;">♥</span> In Wishlist`
                : `<span style="font-size: 1.2em;">♡</span> Add to Wishlist`;

            return;
        }

        // Каталог
        if (btn.classList.contains('product-card__wishlist')) {

            const svg = btn.querySelector('svg');

            if (!svg) return;

            svg.setAttribute(
                'fill',
                isInWishlist ? '#3b82f6' : 'none'
            );

            svg.setAttribute(
                'stroke',
                isInWishlist ? '#3b82f6' : '#64748b'
            );

            btn.setAttribute(
                'aria-label',
                isInWishlist
                    ? 'Remove from wishlist'
                    : 'Add to wishlist'
            );
        }
    }

    window.addEventListener('pageshow', function (event) {
        if (event.persisted) {
            window.location.reload();
        }
    });

    function getCookie(name) {
        let cookieValue = null;

        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');

            for (let cookie of cookies) {
                const cookieTrimmed = cookie.trim();

                if (cookieTrimmed.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(
                        cookieTrimmed.substring(name.length + 1)
                    );
                    break;
                }
            }
        }

        return cookieValue;
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