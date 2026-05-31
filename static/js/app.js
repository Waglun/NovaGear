/**
 * NovaGear — Homepage
 */
(function () {
  "use strict";

  function renderFeatured() {
    const grid = document.querySelector("[data-products-grid]");
    if (!grid || typeof NOVAGEAR_PRODUCTS === "undefined") return;
    NovaGearUI.renderProductGrid(grid, NOVAGEAR_PRODUCTS.slice(0, 8));
  }

  function bindNewsletter() {
    const form = document.querySelector("[data-newsletter-form]");
    const msg = document.querySelector("[data-newsletter-message]");
    if (!form) return;

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const input = form.querySelector("input[type=email]");
      const email = input?.value.trim();

      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        if (msg) {
          msg.textContent = "Please enter a valid email address.";
          msg.classList.add("is-error");
        }
        return;
      }
      if (msg) {
        msg.textContent = "You're in! Check your inbox for a welcome offer.";
        msg.classList.remove("is-error");
      }
      input.value = "";
      NovaGear.showToast("Subscribed to NovaGear newsletter");
    });
  }

  function init() {
    renderFeatured();
    bindNewsletter();
  }

  document.addEventListener("DOMContentLoaded", () => {
    if (document.body.dataset.page === "home") init();
  });
})();
