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

    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const input = form.querySelector("input[type=email]");
      const email = input?.value.trim();

      // Проверка email на клиенте
      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
          if (msg) {
              msg.textContent = "Please enter a valid email address.";
              msg.classList.add("is-error");
          }
          return;
      }

      try {
          const formData = new FormData(form);

          const response = await fetch(form.action, {
              method: "POST",
              body: formData,
              headers: {
                  "X-Requested-With": "XMLHttpRequest",
              },
          });

          const data = await response.json();

          if (msg) {
              msg.textContent = data.message;
              msg.classList.toggle("is-error", !data.success);
          }

          if (data.success) {
              form.reset();

              if (typeof NovaGear !== "undefined" && NovaGear.showToast) {
                  NovaGear.showToast("Subscribed to NovaGear newsletter");
              }
          }

      } catch (error) {
          console.error("Newsletter error:", error);

          if (msg) {
              msg.textContent = "Something went wrong. Please try again.";
              msg.classList.add("is-error");
          }
      }
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
