/**
 * NovaGear — User profile
 */
(function () {
  "use strict";

  const MOCK_ORDERS = [
    { id: "NG-10482", date: "2026-05-12", status: "Delivered", total: 239.97 },
    { id: "NG-10301", date: "2026-04-03", status: "Shipped", total: 89.99 },
    { id: "NG-09877", date: "2026-02-18", status: "Delivered", total: 149.99 },
  ];

  function requireAuth() {
    if (!NovaGear.isLoggedIn()) {
      window.location.href = "/accounts/login/?next=/accounts/profile/";
      return false;
    }
    return true;
  }


  function renderOrders() {
    const tbody = document.querySelector("[data-orders-body]");
    if (!tbody) return;

    tbody.innerHTML = MOCK_ORDERS.map(
      (o) => `
      <tr>
        <td><strong>${o.id}</strong></td>
        <td>${o.date}</td>
        <td><span class="status-badge status-badge--${o.status.toLowerCase()}">${o.status}</span></td>
        // <td>${NovaGear.formatPrice(o.total)}</td>
        <td>${o.total}</td>
        <td><a href="order_detail.html?id=${encodeURIComponent(o.id)}" class="btn btn--ghost btn--sm">View</a></td>
      </tr>`
    ).join("");
  }

  function renderWishlistPreview() {
    const el = document.querySelector("[data-profile-wishlist-count]");
    if (el) el.textContent = String(NovaGear.getWishlist().length);
  }

  function bindProfileForm() {
    document.querySelector("[data-profile-form]")?.addEventListener("submit", (e) => {
      e.preventDefault();
      const form = e.target;
      const user = NovaGear.getUser();
      NovaGear.setUser({
        ...user,
        displayName: form.displayName.value.trim(),
        email: form.email.value.trim(),
      });
      NovaGear.showToast("Profile updated");
    });
  }

  function bindTabs() {
    document.querySelectorAll("[data-profile-tab]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const tab = btn.dataset.profileTab;
        document.querySelectorAll("[data-profile-tab]").forEach((b) => {
          b.classList.toggle("profile-nav__item--active", b.dataset.profileTab === tab);
        });
        document.querySelectorAll("[data-profile-panel]").forEach((p) => {
          p.hidden = p.dataset.profilePanel !== tab;
        });
      });
    });
  }

  function init() {
    if (document.body.dataset.page !== "profile") return;

    renderOrders();
    renderWishlistPreview();
    bindProfileForm();
    bindTabs();

  }

  document.addEventListener("DOMContentLoaded", init);
})();
