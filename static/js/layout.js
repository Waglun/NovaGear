/**
 * NovaGear — Shared header & footer
 */
(function () {
  "use strict";

  const PAGES = {
    home: { home: true },
    catalog: { catalog: true },
    cart: { cart: true },
    auth: { auth: true },
    profile: { profile: true },
    wishlist: { wishlist: true },
  };

  function navClass(page, key) {
    return PAGES[page]?.[key] ? "nav__link nav__link--active" : "nav__link";
  }

  function renderHeader(page) {
    return `
    <header class="header" id="header">
      <nav class="nav container grid-12" aria-label="Main navigation">
        <a href="index.html" class="nav__logo" aria-label="NovaGear home">
          <span class="nav__logo-icon" aria-hidden="true"></span>
          <span class="nav__logo-text">Nova<span class="text-gradient">Gear</span></span>
        </a>
        <ul class="nav__links" role="list">
          <li><a href="index.html" class="${navClass(page, "home")}">Home</a></li>
          <li><a href="catalog.html" class="${navClass(page, "catalog")}">Catalog</a></li>
          <li><a href="wishlist.html" class="${navClass(page, "wishlist")}">Wishlist</a></li>
          <li>
            <a href="cart.html" class="nav__link nav__link--cart ${page === "cart" ? "nav__link--active" : ""}" aria-label="Shopping cart">
              <svg class="icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg>
              <span class="nav__badge" data-cart-count>0</span>
            </a>
          </li>
        </ul>
        <div class="nav__search">
          <form class="search-form" action="catalog.html" method="get" role="search" aria-label="Site search">
            <svg class="search-form__icon icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
            <input type="search" class="search-form__input" name="q" placeholder="Search gear..." autocomplete="off">
          </form>
        </div>
        <div class="nav__actions">
          <a href="wishlist.html" class="btn btn--ghost btn--icon nav__wishlist-btn" aria-label="Wishlist">
            <svg class="icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>
            <span class="nav__badge nav__badge--wishlist" data-wishlist-count>0</span>
          </a>
          <div class="nav__auth" data-auth-guest>
            <a href="/accounts/login/" class="btn btn--ghost btn--sm">Log in</a>
            <a href="/accounts/register/" class="btn btn--primary btn--sm">Register</a>
          </div>
          <a href="profile.html" class="nav__user" data-auth-user hidden>
            <span class="nav__avatar" data-user-avatar>NG</span>
            <span class="nav__user-name" data-user-name>Account</span>
          </a>
          <button type="button" class="btn btn--ghost nav__menu-toggle" aria-label="Open menu" aria-expanded="false" data-menu-toggle>
            <svg class="icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
          </button>
        </div>
      </nav>
      <div class="nav-drawer" data-nav-drawer hidden>
        <div class="nav-drawer__inner">
          <form class="search-form search-form--full" action="catalog.html" method="get" role="search">
            <input type="search" class="search-form__input" name="q" placeholder="Search gear...">
          </form>
          <ul class="nav-drawer__links" role="list">
            <li><a href="index.html" class="${navClass(page, "home")}">Home</a></li>
            <li><a href="catalog.html" class="${navClass(page, "catalog")}">Catalog</a></li>
            <li><a href="wishlist.html" class="${navClass(page, "wishlist")}">Wishlist</a></li>
            <li><a href="cart.html" class="${navClass(page, "cart")}">Cart</a></li>
            <li><a href="profile.html" class="${navClass(page, "profile")}">Profile</a></li>
          </ul>
          <div class="nav-drawer__auth" data-auth-guest>
            <a href="/accounts/login/" class="btn btn--outline btn--block">Log in</a>
            <a href="/accounts/register/" class="btn btn--primary btn--block">Register</a>
          </div>
          <div class="nav-drawer__auth" data-auth-user hidden>
            <a href="profile.html" class="btn btn--primary btn--block">My Profile</a>
            <button type="button" class="btn btn--outline btn--block" data-logout>Sign out</button>
          </div>
        </div>
      </div>
    </header>`;
  }

  function renderFooter() {
    return `
    <footer class="footer">
      <div class="container">
        <div class="grid-12 footer__top">
          <div class="footer__brand col-span-4">
            <a href="index.html" class="nav__logo footer__logo">
              <span class="nav__logo-icon" aria-hidden="true"></span>
              <span class="nav__logo-text">Nova<span class="text-gradient">Gear</span></span>
            </a>
            <p class="footer__tagline">Premium gaming accessories for the next generation of players and creators.</p>
            <div class="footer__social">
              <a href="#" class="social-link" aria-label="Twitter / X"><svg class="icon" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a>
              <a href="#" class="social-link" aria-label="Discord"><svg class="icon" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.317 4.37a19.791 19.791 0 00-4.885-1.515.074.074 0 00-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 00-5.487 0 12.64 12.64 0 00-.617-1.25.077.077 0 00-.079-.037A19.736 19.736 0 003.677 4.37a.07.07 0 00-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 00.031.057 19.9 19.9 0 005.993 3.03.078.078 0 00.084-.028 14.09 14.09 0 001.226-1.994.076.076 0 00-.041-.106 13.107 13.107 0 01-1.872-.892.077.077 0 01-.008-.128 10.2 10.2 0 00.372-.292.074.074 0 01.077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 01.078.01c.12.098.246.198.373.292a.077.077 0 01-.006.127 12.299 12.299 0 01-1.873.892.077.077 0 00-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 00.084.028 19.839 19.839 0 006.002-3.03.077.077 0 00.032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 00-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/></svg></a>
              <a href="#" class="social-link" aria-label="YouTube"><svg class="icon" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a>
              <a href="#" class="social-link" aria-label="Instagram"><svg class="icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1112.63 8 4 4 0 0116 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg></a>
            </div>
          </div>
          <nav class="footer__nav col-span-2" aria-label="Shop">
            <h3 class="footer__nav-title">Shop</h3>
            <ul role="list">
              <li><a href="catalog.html">All Products</a></li>
              <li><a href="catalog.html#categories">Categories</a></li>
              <li><a href="catalog.html?sort=new">New Arrivals</a></li>
              <li><a href="catalog.html?sort=rating">Best Sellers</a></li>
            </ul>
          </nav>
          <nav class="footer__nav col-span-2" aria-label="Account">
            <h3 class="footer__nav-title">Account</h3>
            <ul role="list">
              <li><a href="login.html">Log in</a></li>
              <li><a href="profile.html">Profile</a></li>
              <li><a href="cart.html">Cart</a></li>
              <li><a href="wishlist.html">Wishlist</a></li>
            </ul>
          </nav>
          <nav class="footer__nav col-span-2" aria-label="Company">
            <h3 class="footer__nav-title">Company</h3>
            <ul role="list">
              <li><a href="#">About Us</a></li>
              <li><a href="#">Shipping</a></li>
              <li><a href="#">Returns</a></li>
              <li><a href="#">Privacy</a></li>
            </ul>
          </nav>
        </div>
        <div class="footer__bottom">
          <p class="footer__copy">&copy; <span data-year></span> NovaGear. All rights reserved.</p>
          <p class="footer__note">Dropshipping model — prices and availability subject to partner inventory.</p>
        </div>
      </div>
    </footer>`;
  }

  function initLayout() {
    const page = document.body.dataset.page || "home";
    const headerSlot = document.querySelector("[data-site-header]");
    const footerSlot = document.querySelector("[data-site-footer]");

    if (headerSlot) headerSlot.innerHTML = renderHeader(page);
    if (footerSlot) footerSlot.innerHTML = renderFooter();

    NovaGear.initBase();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initLayout);
  } else {
    initLayout();
  }
})();

