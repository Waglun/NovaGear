/**
 * NovaGear — Shared state & helpers
 */
const NovaGear = {
  STORAGE_CART: "novagear_cart",
  STORAGE_WISHLIST: "novagear_wishlist",

  getCart() {
    try {
      return JSON.parse(localStorage.getItem(this.STORAGE_CART)) || [];
    } catch {
      return [];
    }
  },

  setCart(items) {
    localStorage.setItem(this.STORAGE_CART, JSON.stringify(items));
    this.updateCartBadge();
  },

  getWishlist() {
    try {
      return JSON.parse(localStorage.getItem(this.STORAGE_WISHLIST)) || [];
    } catch {
      return [];
    }
  },

  setWishlist(ids) {
    localStorage.setItem(this.STORAGE_WISHLIST, JSON.stringify(ids));
    this.updateWishlistBadge();
    this.syncWishlistButtons();
  },

  getProductById(id) {
    if (typeof NOVAGEAR_PRODUCTS === "undefined") return null;
    return NOVAGEAR_PRODUCTS.find((p) => p.id === id) || null;
  },

  formatPrice(value) {
    return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(value);
  },

  renderStars(rating) {
    const full = Math.floor(rating);
    const half = rating % 1 >= 0.5;
    let stars = "";
    for (let i = 0; i < 5; i++) {
      if (i < full) stars += "★";
      else if (i === full && half) stars += "★";
      else stars += "☆";
    }
    return stars;
  },

  showToast(message) {
    const toast = document.querySelector("[data-toast]");
    const msgEl = document.querySelector("[data-toast-message]");
    if (!toast || !msgEl) return;

    msgEl.textContent = message;
    toast.removeAttribute("hidden");
    toast.classList.add("is-visible");

    clearTimeout(NovaGear._toastTimer);
    NovaGear._toastTimer = setTimeout(() => {
      toast.classList.remove("is-visible");
      setTimeout(() => toast.setAttribute("hidden", ""), 300);
    }, 2800);
  },

  updateCartBadge() {
    const count = this.getCart().reduce((sum, item) => sum + item.qty, 0);
    document.querySelectorAll("[data-cart-count]").forEach((el) => {
      el.textContent = count;
      el.dataset.count = count;
      el.style.display = count > 0 ? "" : "none";
    });
  },

  updateWishlistBadge() {
    const ids = this.getWishlist();
    document.querySelectorAll("[data-wishlist-count]").forEach((el) => {
      el.textContent = ids.length;
      el.dataset.count = ids.length;
      el.style.display = ids.length > 0 ? "" : "none";
    });
  },

  syncWishlistButtons() {
    const ids = this.getWishlist();
    document.querySelectorAll("[data-wishlist-id]").forEach((btn) => {
      const active = ids.includes(btn.dataset.wishlistId);
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", String(active));
    });
  },

  addToCart(productId, qty = 1) {
    const product = this.getProductById(productId);
    if (!product) return false;

    const cart = this.getCart();
    const existing = cart.find((item) => item.id === productId);
    if (existing) {
      existing.qty += qty;
    } else {
      cart.push({
        id: productId,
        name: product.name,
        price: product.price,
        imageClass: product.imageClass,
        qty,
      });
    }
    this.setCart(cart);
    this.showToast(`${product.name} added to cart`);
    return true;
  },

  toggleWishlist(productId) {
    const ids = this.getWishlist();
    const index = ids.indexOf(productId);
    const product = this.getProductById(productId);

    if (index === -1) {
      ids.push(productId);
      if (product) this.showToast(`${product.name} added to wishlist`);
    } else {
      ids.splice(index, 1);
      if (product) this.showToast(`${product.name} removed from wishlist`);
    }
    this.setWishlist(ids);
  },

  bindProductActions() {
    document.addEventListener("click", (e) => {
      const cartBtn = e.target.closest("[data-add-cart]");
      if (cartBtn) {
        e.preventDefault();
        this.addToCart(cartBtn.dataset.addCart);
        return;
      }
      const wishBtn = e.target.closest("[data-wishlist-id]");
      if (wishBtn) {
        e.preventDefault();
        this.toggleWishlist(wishBtn.dataset.wishlistId);
      }
    });
  },

  bindCommonUI() {
    const menuToggle = document.querySelector("[data-menu-toggle]");
    const drawer = document.querySelector("[data-nav-drawer]");

    if (menuToggle && drawer) {
      menuToggle.addEventListener("click", () => {
        const isOpen = !drawer.hidden;
        drawer.hidden = isOpen;
        menuToggle.setAttribute("aria-expanded", String(!isOpen));
        menuToggle.setAttribute("aria-label", isOpen ? "Open menu" : "Close menu");
        document.body.classList.toggle("nav-open", !isOpen);
      });

      drawer.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
          drawer.hidden = true;
          menuToggle.setAttribute("aria-expanded", "false");
          document.body.classList.remove("nav-open");
        });
      });
    }

    const header = document.getElementById("header");
    if (header) {
      window.addEventListener(
        "scroll",
        () => header.classList.toggle("is-scrolled", window.scrollY > 8),
        { passive: true }
      );
    }

    const yearEl = document.querySelector("[data-year]");
    if (yearEl) yearEl.textContent = new Date().getFullYear();

    document.querySelector("[data-logout]")?.addEventListener("click", (e) => {
      e.preventDefault();
      this.setUser(null);
      this.showToast("Signed out successfully");
      setTimeout(() => {
        window.location.href = "index.html";
      }, 600);
    });
  },

  initBase() {
    this.updateCartBadge();
    this.updateWishlistBadge();
    this.syncWishlistButtons();
    this.updateAuthUI();
    this.bindProductActions();
    this.bindCommonUI();
  },
};
