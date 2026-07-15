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

