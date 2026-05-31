/**
 * NovaGear — Wishlist page
 */
(function () {
  "use strict";

  function render() {
    const grid = document.querySelector("[data-wishlist-grid]");
    const empty = document.querySelector("[data-wishlist-empty]");
    if (!grid) return;

    const ids = NovaGear.getWishlist();
    const products = ids.map((id) => NovaGear.getProductById(id)).filter(Boolean);

    if (!products.length) {
      grid.innerHTML = "";
      if (empty) empty.hidden = false;
      return;
    }

    if (empty) empty.hidden = true;
    NovaGearUI.renderProductGrid(grid, products);
  }

  function init() {
    if (document.body.dataset.page !== "wishlist") return;
    render();
    window.addEventListener("storage", render);
    document.addEventListener("click", (e) => {
      if (e.target.closest("[data-wishlist-id]")) {
        setTimeout(render, 50);
      }
    });
  }

  document.addEventListener("DOMContentLoaded", init);
})();
