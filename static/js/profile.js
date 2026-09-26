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

  function getAllOrders() {
    const stored = NovaGear.getOrders().map((o) => ({
      id: o.id,
      date: o.date,
      status: o.status,
      total: o.total,
    }));
    const storedIds = new Set(stored.map((o) => o.id));
    const merged = [...stored, ...MOCK_ORDERS.filter((o) => !storedIds.has(o.id))];
    return merged.sort((a, b) => b.date.localeCompare(a.date));
  }

  function bindTabs() {
    const buttons = document.querySelectorAll("[data-profile-tab]");
    const panels = document.querySelectorAll("[data-profile-panel]");

    function activateTab(tab) {
      buttons.forEach((btn) => {
        btn.classList.toggle(
          "profile-nav__item--active",
          btn.dataset.profileTab === tab
        );
      });

      panels.forEach((panel) => {
        panel.hidden = panel.dataset.profilePanel !== tab;
      });
    }

    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const tab = btn.dataset.profileTab;

        activateTab(tab);
      });
    });

    // Определяем вкладку из URL
    const params = new URLSearchParams(window.location.search);
    const tabFromUrl = params.get("tab");

    // Если в URL нет tab — используем overview
    activateTab(tabFromUrl || "overview");
  }

  function init() {
    if (document.body.dataset.page !== "profile") return;

    bindTabs();

  }

  document.addEventListener("DOMContentLoaded", init);
})();
