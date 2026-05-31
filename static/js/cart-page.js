/**
 * NovaGear — Cart page
 */
(function () {
  "use strict";

  function renderCart() {
    const container = document.querySelector("[data-cart-content]");
    const summary = document.querySelector("[data-cart-summary]");
    if (!container) return;

    const cart = NovaGear.getCart();

    if (!cart.length) {
      container.innerHTML = `
        <div class="empty-state empty-state--large">
          <div class="empty-state__icon" aria-hidden="true">🛒</div>
          <h2>Your cart is empty</h2>
          <p>Looks like you haven't added any gear yet.</p>
          <a href="catalog.html" class="btn btn--primary">Browse catalog</a>
        </div>`;
      if (summary) summary.hidden = true;
      return;
    }

    if (summary) summary.hidden = false;

    container.innerHTML = `
      <div class="cart-table-wrap">
        <table class="cart-table">
          <thead>
            <tr>
              <th>Product</th>
              <th>Price</th>
              <th>Quantity</th>
              <th>Total</th>
              <th><span class="visually-hidden">Remove</span></th>
            </tr>
          </thead>
          <tbody>
            ${cart
              .map(
                (item) => `
              <tr data-cart-row="${item.id}">
                <td class="cart-table__product">
                  <div class="cart-item">
                    <div class="cart-item__img product-card__img--placeholder ${item.imageClass || ""}"></div>
                    <span class="cart-item__name">${item.name}</span>
                  </div>
                </td>
                <td>${NovaGear.formatPrice(item.price)}</td>
                <td>
                  <div class="qty-control">
                    <button type="button" class="qty-control__btn" data-qty-minus="${item.id}" aria-label="Decrease quantity">−</button>
                    <span class="qty-control__value" data-qty-value="${item.id}">${item.qty}</span>
                    <button type="button" class="qty-control__btn" data-qty-plus="${item.id}" aria-label="Increase quantity">+</button>
                  </div>
                </td>
                <td class="cart-table__total" data-line-total="${item.id}">${NovaGear.formatPrice(item.price * item.qty)}</td>
                <td>
                  <button type="button" class="btn btn--ghost btn--sm" data-remove-cart="${item.id}" aria-label="Remove item">Remove</button>
                </td>
              </tr>`
              )
              .join("")}
          </tbody>
        </table>
      </div>`;

    updateSummary(cart);
  }

  function updateSummary(cart) {
    const subtotal = cart.reduce((s, i) => s + i.price * i.qty, 0);
    const shipping = subtotal > 99 ? 0 : 9.99;
    const total = subtotal + shipping;

    document.querySelector("[data-cart-subtotal]")?.replaceChildren(
      document.createTextNode(NovaGear.formatPrice(subtotal))
    );
    document.querySelector("[data-cart-shipping]")?.replaceChildren(
      document.createTextNode(shipping === 0 ? "Free" : NovaGear.formatPrice(shipping))
    );
    document.querySelector("[data-cart-total]")?.replaceChildren(
      document.createTextNode(NovaGear.formatPrice(total))
    );
  }

  function updateQty(productId, delta) {
    const cart = NovaGear.getCart();
    const item = cart.find((i) => i.id === productId);
    if (!item) return;

    item.qty += delta;
    if (item.qty <= 0) {
      NovaGear.setCart(cart.filter((i) => i.id !== productId));
    } else {
      NovaGear.setCart(cart);
    }
    renderCart();
  }

  function bindEvents() {
    document.addEventListener("click", (e) => {
      const plus = e.target.closest("[data-qty-plus]");
      if (plus) {
        updateQty(plus.dataset.qtyPlus, 1);
        return;
      }
      const minus = e.target.closest("[data-qty-minus]");
      if (minus) {
        updateQty(minus.dataset.qtyMinus, -1);
        return;
      }
      const remove = e.target.closest("[data-remove-cart]");
      if (remove) {
        const id = remove.dataset.removeCart;
        NovaGear.setCart(NovaGear.getCart().filter((i) => i.id !== id));
        NovaGear.showToast("Item removed from cart");
        renderCart();
      }
    });

    document.querySelector("[data-checkout]")?.addEventListener("click", () => {
      if (!NovaGear.getCart().length) return;
      if (!NovaGear.isLoggedIn()) {
        NovaGear.showToast("Please sign in to checkout");
        setTimeout(() => {
          window.location.href = "login.html?next=cart.html";
        }, 800);
        return;
      }
      NovaGear.showToast("Checkout demo — connect to Django payment flow");
    });
  }

  function init() {
    if (document.body.dataset.page !== "cart") return;
    bindEvents();
    renderCart();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
