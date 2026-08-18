/**
 * NovaGear — Order detail page
 * Mirrors Django order_detail view: order with prefetched items__product
 */
(function () {
  "use strict";

  const MOCK_ORDERS = {
    "NG-10482": {
      id: "NG-10482",
      date: "2026-05-12",
      status: "Delivered",
      address: "г. Москва, ул. Тверская, д. 12, кв. 45",
      phone: "+7 (999) 123-45-67",
      comment: "Позвонить за час до доставки",
      items: [
        { name: "ProMouse X1", price: 79.99, qty: 2, imageClass: "product-card__img--mouse-1" },
        { name: "NovaKey TKL", price: 79.99, qty: 1, imageClass: "product-card__img--keyboard-1" },
      ],
    },
    "NG-10301": {
      id: "NG-10301",
      date: "2026-04-03",
      status: "Shipped",
      address: "г. Санкт-Петербург, Невский пр., д. 28",
      phone: "+7 (921) 555-00-11",
      comment: "",
      items: [{ name: "PulseHeadset Pro", price: 89.99, qty: 1, imageClass: "product-card__img--headset-1" }],
    },
    "NG-09877": {
      id: "NG-09877",
      date: "2026-02-18",
      status: "Delivered",
      address: "г. Казань, ул. Баумана, д. 7",
      phone: "+7 (843) 200-30-40",
      comment: "",
      items: [{ name: "StreamCam 4K", price: 149.99, qty: 1, imageClass: "product-card__img--stream-1" }],
    },
  };

  const STATUS_CLASS = {
    delivered: "status-badge--delivered",
    shipped: "status-badge--shipped",
    processing: "status-badge--processing",
    pending: "status-badge--pending",
    cancelled: "status-badge--cancelled",
  };

  function calcTotals(items) {
    const subtotal = items.reduce((sum, item) => sum + item.price * item.qty, 0);
    const shipping = subtotal > 99 ? 0 : 9.99;
    return { subtotal, shipping, total: subtotal + shipping };
  }

  function formatDate(isoDate) {
    return new Intl.DateTimeFormat("ru-RU", {
      day: "numeric",
      month: "long",
      year: "numeric",
    }).format(new Date(isoDate));
  }

  function getOrderIdFromUrl() {
    return new URLSearchParams(window.location.search).get("id");
  }

  function requireAuth() {
    if (!NovaGear.isLoggedIn()) {
      const next = encodeURIComponent(window.location.pathname + window.location.search);
      window.location.href = `login.html?next=${next}`;
      return false;
    }
    return true;
  }

  function renderNotFound() {
    const main = document.querySelector(".order-detail-page .container");
    if (!main) return;

    main.innerHTML = `
      <div class="empty-state empty-state--large">
        <div class="empty-state__icon" aria-hidden="true">📦</div>
        <h2>Заказ не найден</h2>
        <p>Проверьте номер заказа или вернитесь в личный кабинет.</p>
        <a href="profile.html" class="btn btn--primary">К заказам</a>
      </div>`;
  }

  function renderItems(items) {
    const tbody = document.querySelector("[data-order-items]");
    if (!tbody) return;

    tbody.innerHTML = items
      .map(
        (item) => `
        <tr>
          <td>
            <div class="cart-item">
              <div class="cart-item__img product-card__img--placeholder ${item.imageClass || ""}"></div>
              <span class="cart-item__name">${item.name}</span>
            </div>
          </td>
          <td>${NovaGear.formatPrice(item.price)}</td>
          <td>${item.qty}</td>
          <td class="cart-table__total">${NovaGear.formatPrice(item.price * item.qty)}</td>
        </tr>`
      )
      .join("");
  }

  function renderOrder(order) {
    const { subtotal, shipping, total } = calcTotals(order.items);
    const statusKey = order.status.toLowerCase();

    document.querySelector("[data-order-breadcrumb]")?.replaceChildren(
      document.createTextNode(`Заказ #${order.id}`)
    );
    document.querySelector("[data-order-id]")?.replaceChildren(document.createTextNode(`#${order.id}`));
    document.querySelector("[data-order-date]")?.replaceChildren(
      document.createTextNode(`Оформлен ${formatDate(order.date)}`)
    );

    const statusEl = document.querySelector("[data-order-status]");
    if (statusEl) {
      statusEl.textContent = order.status;
      statusEl.className = `status-badge ${STATUS_CLASS[statusKey] || "status-badge--pending"}`;
      statusEl.hidden = false;
    }

    document.querySelector("[data-order-address]")?.replaceChildren(document.createTextNode(order.address));
    document.querySelector("[data-order-phone]")?.replaceChildren(document.createTextNode(order.phone));

    const commentRow = document.querySelector("[data-order-comment-row]");
    const commentEl = document.querySelector("[data-order-comment]");
    if (order.comment) {
      commentEl?.replaceChildren(document.createTextNode(order.comment));
      if (commentRow) commentRow.hidden = false;
    }

    document.querySelector("[data-order-subtotal]")?.replaceChildren(
      document.createTextNode(NovaGear.formatPrice(subtotal))
    );
    document.querySelector("[data-order-shipping]")?.replaceChildren(
      document.createTextNode(shipping === 0 ? "Бесплатно" : NovaGear.formatPrice(shipping))
    );
    document.querySelector("[data-order-total]")?.replaceChildren(
      document.createTextNode(NovaGear.formatPrice(total))
    );

    document.title = `Заказ #${order.id} — NovaGear`;
    renderItems(order.items);
  }

  function init() {
    if (document.body.dataset.page !== "order-detail") return;
    if (!requireAuth()) return;

    const orderId = getOrderIdFromUrl();
    const order = orderId ? MOCK_ORDERS[orderId] : null;

    if (!order) {
      renderNotFound();
      return;
    }

    renderOrder(order);
  }

  document.addEventListener("DOMContentLoaded", init);
})();
