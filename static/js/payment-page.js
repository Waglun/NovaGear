/**
 * NovaGear — Payment page (demo simulation)
 */
(function () {
  "use strict";

  function calcTotals(cart) {
    const subtotal = cart.reduce((s, i) => s + i.price * i.qty, 0);
    const shipping = subtotal > 99 ? 0 : 9.99;
    const total = subtotal + shipping;
    return { subtotal, shipping, total };
  }

function requirePaymentAccess() {
  return true;
}

function renderDelivery(pending) {
  const section = document.querySelector("[data-payment-delivery]");

  if (!pending) {
    if (section) section.hidden = true;
    return;
  }

  document.querySelector("[data-payment-address]")?.replaceChildren(
    document.createTextNode(pending.address)
  );

  document.querySelector("[data-payment-phone]")?.replaceChildren(
    document.createTextNode(pending.phone)
  );

  if (section) section.hidden = false;
}
  function renderItems(cart) {
    const list = document.querySelector("[data-payment-items]");
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

    document.querySelector("[data-payment-subtotal]")?.replaceChildren(
      document.createTextNode(NovaGear.formatPrice(subtotal))
    );
    document.querySelector("[data-payment-shipping]")?.replaceChildren(
      document.createTextNode(shipping === 0 ? "Бесплатно" : NovaGear.formatPrice(shipping))
    );
    document.querySelector("[data-payment-total]")?.replaceChildren(
      document.createTextNode(NovaGear.formatPrice(total))
    );
    document.querySelector("[data-payment-submit-amount]")?.replaceChildren(
      document.createTextNode(NovaGear.formatPrice(total))
    );

    return total;
  }

  function formatCardNumber(value) {
    const digits = value.replace(/\D/g, "").slice(0, 16);
    return digits.replace(/(\d{4})(?=\d)/g, "$1 ").trim();
  }

  function formatExpiry(value) {
    const digits = value.replace(/\D/g, "").slice(0, 4);
    if (digits.length <= 2) return digits;
    return `${digits.slice(0, 2)}/${digits.slice(2)}`;
  }

  function bindInputMasks() {
    const numberInput = document.getElementById("id_card_number");
    const expiryInput = document.getElementById("id_card_expiry");
    const cvvInput = document.getElementById("id_card_cvv");

    numberInput?.addEventListener("input", () => {
      numberInput.value = formatCardNumber(numberInput.value);
    });

    expiryInput?.addEventListener("input", () => {
      expiryInput.value = formatExpiry(expiryInput.value);
    });

    cvvInput?.addEventListener("input", () => {
      cvvInput.value = cvvInput.value.replace(/\D/g, "").slice(0, 4);
    });
  }

  function bindMethodToggle() {
    const cardFields = document.querySelector("[data-payment-card-fields]");
    const walletNote = document.querySelector("[data-payment-wallet-note]");
    const methods = document.querySelectorAll("[data-payment-method]");

    methods.forEach((input) => {
      input.addEventListener("change", () => {
        const isCard = input.value === "card" && input.checked;
        if (cardFields) cardFields.hidden = !isCard;
        if (walletNote) walletNote.hidden = isCard;
      });
    });
  }

  function validateCard(form) {
    const name = form.card_name.value.trim();
    const number = form.card_number.value.replace(/\s/g, "");
    const expiry = form.card_expiry.value.trim();
    const cvv = form.card_cvv.value.trim();

    if (!name) {
      NovaGear.showToast("Введите имя на карте");
      return false;
    }
    if (number.length < 16) {
      NovaGear.showToast("Введите корректный номер карты");
      return false;
    }
    if (!/^\d{2}\/\d{2}$/.test(expiry)) {
      NovaGear.showToast("Введите срок действия в формате MM/YY");
      return false;
    }
    if (cvv.length < 3) {
      NovaGear.showToast("Введите CVV-код");
      return false;
    }
    return true;
  }

  function showOverlay(title, desc) {
    const overlay = document.querySelector("[data-payment-overlay]");
    document.querySelector("[data-payment-overlay-title]")?.replaceChildren(
      document.createTextNode(title)
    );
    document.querySelector("[data-payment-overlay-desc]")?.replaceChildren(
      document.createTextNode(desc)
    );
    if (overlay) {
      overlay.hidden = false;
      overlay.setAttribute("aria-hidden", "false");
    }
  }

  function hideOverlay() {
    const overlay = document.querySelector("[data-payment-overlay]");
    if (overlay) {
      overlay.hidden = true;
      overlay.setAttribute("aria-hidden", "true");
    }
  }

  function getPaymentMethodLabel(method) {
    if (method === "apple") return "Apple Pay";
    if (method === "google") return "Google Pay";
    return "картой";
  }

  function createOrder(cart, pending, method) {
    const { subtotal, shipping, total } = calcTotals(cart);
    const orderId = NovaGear.generateOrderId();

    return NovaGear.addOrder({
      id: orderId,
      date: new Date().toISOString().slice(0, 10),
      status: "Processing",
      address: pending.address,
      phone: pending.phone,
      comment: pending.comment || "",
      paymentMethod: method,
      items: cart.map((item) => ({
        name: item.name,
        price: item.price,
        qty: item.qty,
        imageClass: item.imageClass,
      })),
      subtotal,
      shipping,
      total,
    });
  }

  function simulatePayment(method, onComplete) {
    const label = getPaymentMethodLabel(method);
    showOverlay("Обработка платежа…", `Имитация оплаты ${label}`);

    setTimeout(() => {
      showOverlay("Платёж принят", "Создаём заказ…");
      setTimeout(onComplete, 900);
    }, 1800);
  }

  function bindForm() {
    const form = document.querySelector("[data-payment-form]");
    const submitBtn = document.querySelector("[data-payment-submit]");
    if (!form) return;

    form.addEventListener("submit", (e) => {
      e.preventDefault();

      const method = form.payment_method.value;
      if (method === "card" && !validateCard(form)) return;

      submitBtn.disabled = true;

      simulatePayment(method, () => {
        const cart = NovaGear.getCart();
        const pending = NovaGear.getPendingCheckout();
        const order = createOrder(cart, pending, method);

        NovaGear.setCart([]);
        NovaGear.clearPendingCheckout();
        hideOverlay();
        NovaGear.showToast("Оплата прошла успешно!");

        setTimeout(() => {
          window.location.href = `order_detail.html?id=${encodeURIComponent(order.id)}`;
        }, 700);
      });
    });
  }

  function init() {
    if (document.body.dataset.page !== "payment") return;
    if (!requirePaymentAccess()) return;

    const pending = NovaGear.getPendingCheckout();
    const cart = NovaGear.getCart();

    renderDelivery(pending);
    renderItems(cart);
    renderSummary(cart);
    bindInputMasks();
    bindMethodToggle();
    bindForm();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
