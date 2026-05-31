/**
 * NovaGear — Catalog page
 */
(function () {
  "use strict";

  const CATEGORY_MAP = {
    mice: "Gaming Mice",
    keyboards: "Keyboards",
    headsets: "Headsets",
    mousepads: "Mousepads",
    rgb: "RGB Accessories",
    streaming: "Streaming Gear",
    desk: "Desk Setup",
  };

  const state = {
    category: "",
    sort: "featured",
    search: "",
    maxPrice: Infinity,
  };

  function parseURL() {
    const params = new URLSearchParams(window.location.search);
    const cat = params.get("category");
    state.category = cat && CATEGORY_MAP[cat] ? CATEGORY_MAP[cat] : "";
    state.sort = params.get("sort") || "featured";
    state.search = (params.get("q") || "").trim().toLowerCase();
    const price = params.get("maxPrice");
    state.maxPrice = price ? Number(price) : Infinity;
  }

  function filterProducts() {
    return NOVAGEAR_PRODUCTS.filter((p) => {
      if (state.category && p.category !== state.category) return false;
      if (state.search && !p.name.toLowerCase().includes(state.search) && !p.category.toLowerCase().includes(state.search)) return false;
      if (p.price > state.maxPrice) return false;
      return true;
    });
  }

  function sortProducts(products) {
    const list = [...products];
    switch (state.sort) {
      case "price-asc":
        return list.sort((a, b) => a.price - b.price);
      case "price-desc":
        return list.sort((a, b) => b.price - a.price);
      case "rating":
        return list.sort((a, b) => b.rating - a.rating);
      case "new":
        return list.reverse();
      default:
        return list;
    }
  }

  function syncFiltersUI() {
    document.querySelectorAll("[data-filter-category]").forEach((btn) => {
      const slug = btn.dataset.filterCategory;
      const catName = slug ? CATEGORY_MAP[slug] : "";
      btn.classList.toggle("filter-chip--active", state.category === catName);
    });

    const sortSelect = document.querySelector("[data-catalog-sort]");
    if (sortSelect) sortSelect.value = state.sort;

    const searchInput = document.querySelector("[data-catalog-search]");
    if (searchInput) searchInput.value = state.search;

    const countEl = document.querySelector("[data-results-count]");
    if (countEl) {
      const filtered = sortProducts(filterProducts());
      countEl.textContent = `${filtered.length} product${filtered.length !== 1 ? "s" : ""}`;
    }
  }

  function render() {
    const grid = document.querySelector("[data-catalog-grid]");
    const products = sortProducts(filterProducts());
    NovaGearUI.renderProductGrid(grid, products);
    syncFiltersUI();
  }

  function bindFilters() {
    document.querySelectorAll("[data-filter-category]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const slug = btn.dataset.filterCategory;
        state.category = slug ? CATEGORY_MAP[slug] : "";
        render();
      });
    });

    document.querySelector("[data-catalog-sort]")?.addEventListener("change", (e) => {
      state.sort = e.target.value;
      render();
    });

    document.querySelector("[data-catalog-search]")?.addEventListener(
      "input",
      debounce((e) => {
        state.search = e.target.value.trim().toLowerCase();
        render();
      }, 300)
    );

    document.querySelector("[data-price-filter]")?.addEventListener("change", (e) => {
      const val = e.target.value;
      state.maxPrice = val ? Number(val) : Infinity;
      render();
    });
  }

  function debounce(fn, ms) {
    let t;
    return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), ms);
    };
  }

  function init() {
    if (!document.body.dataset.page === "catalog") return;
    parseURL();
    bindFilters();
    render();

    if (state.category) {
      document.querySelector("[data-active-category]")?.replaceChildren(
        document.createTextNode(state.category)
      );
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    if (document.body.dataset.page === "catalog") init();
  });
})();
