/**
 * NovaGear — Checkout page
 * Mirrors Django checkout view: cart_items, total_price, OrderForm
 */
(function () {
  "use strict";

  function calcTotals(cart) {
    const subtotal = cart.reduce((s, i) => s + i.price * i.qty, 0);
    const shipping = subtotal > 99 ? 0 : 9.99;
    const total = subtotal + shipping;
    return { subtotal, shipping, total };
  }

  function requireCheckoutAccess() {
    if (!NovaGear.isLoggedIn()) {
      window.location.href = "login.html?next=checkout.html";
      return false;
    }
    if (!NovaGear.getCart().length) {
      window.location.href = "cart.html";
      return false;
    }
    return true;
  }

  function renderItems(cart) {
    const list = document.querySelector("[data-checkout-items]");
    if (!list) return;

    list.innerHTML = cart
      .map(
        (item) => `
        <li class="checkout-item">
          <div class="checkout-item__img product-card__img--placeholder ${item.imageClass || ""}"></div>
          <div class="checkout-item__info">
            <span class="checkout-item__name">${item.name}</span>
            <span class="checkout-item__meta">${item.qty} × ${NovaGear.formatPrice(item.price)}</span>
          </div>
          <span class="checkout-item__line-total">${NovaGear.formatPrice(item.price * item.qty)}</span>
        </li>`
      )
      .join("");
  }

  function renderSummary(cart) {
    const { subtotal, shipping, total } = calcTotals(cart);

    document.querySelector("[data-checkout-subtotal]")?.replaceChildren(
      document.createTextNode(NovaGear.formatPrice(subtotal))
    );
    document.querySelector("[data-checkout-shipping]")?.replaceChildren(
      document.createTextNode(shipping === 0 ? "Бесплатно" : NovaGear.formatPrice(shipping))
    );
    document.querySelector("[data-checkout-total]")?.replaceChildren(
      document.createTextNode(NovaGear.formatPrice(total))
    );

    const totalInput = document.getElementById("id_total_price");
    if (totalInput) totalInput.value = total.toFixed(2);

    return total;
  }

  function bindForm() {
    const form = document.querySelector("[data-checkout-form]");
    if (!form) return;

    form.addEventListener("submit", (e) => {
      e.preventDefault();

      const address = form.address.value.trim();
      const phone = form.phone.value.trim();

      if (!address || !phone) {
        NovaGear.showToast("Заполните адрес и телефон");
        return;
      }

      const cart = NovaGear.getCart();
      const { total } = calcTotals(cart);

      NovaGear.setPendingCheckout({
        address,
        phone,
        comment: form.comment.value.trim(),
        totalPrice: total,
      });

      window.location.href = "payment.html";
    });
  }

  function init() {
    if (document.body.dataset.page !== "checkout") return;
    if (!requireCheckoutAccess()) return;

    const cart = NovaGear.getCart();
    renderItems(cart);
    renderSummary(cart);
    bindForm();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
