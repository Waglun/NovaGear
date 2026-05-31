/**
 * NovaGear — Login & Register
 */
(function () {
  "use strict";

  function switchTab(tab) {
    document.querySelectorAll("[data-auth-tab]").forEach((btn) => {
      const active = btn.dataset.authTab === tab;
      btn.classList.toggle("tabs__btn--active", active);
      btn.setAttribute("aria-selected", String(active));
    });
    document.querySelectorAll("[data-auth-panel]").forEach((panel) => {
      panel.hidden = panel.dataset.authPanel !== tab;
    });
  }

  function bindTabs() {
    document.querySelectorAll("[data-auth-tab]").forEach((btn) => {
      btn.addEventListener("click", () => switchTab(btn.dataset.authTab));
    });

    if (window.location.hash === "#register") {
      switchTab("register");
    }
  }

  function bindLogin() {
    document.querySelector("[data-login-form]")?.addEventListener("submit", (e) => {
      e.preventDefault();
      const form = e.target;
      const email = form.email.value.trim();
      const password = form.password.value;

      if (!email || !password) {
        NovaGear.showToast("Please fill in all fields");
        return;
      }

      NovaGear.setUser({
        email,
        displayName: email.split("@")[0],
        memberSince: new Date().toISOString().slice(0, 10),
      });

      NovaGear.showToast("Welcome back!");
      redirectAfterAuth();
    });
  }

  function bindRegister() {
    document.querySelector("[data-register-form]")?.addEventListener("submit", (e) => {
      e.preventDefault();
      const form = e.target;
      const name = form.displayName.value.trim();
      const email = form.email.value.trim();
      const password = form.password.value;
      const confirm = form.passwordConfirm.value;

      if (!name || !email || !password) {
        NovaGear.showToast("Please fill in all fields");
        return;
      }
      if (password.length < 6) {
        NovaGear.showToast("Password must be at least 6 characters");
        return;
      }
      if (password !== confirm) {
        NovaGear.showToast("Passwords do not match");
        return;
      }

      NovaGear.setUser({
        email,
        displayName: name,
        memberSince: new Date().toISOString().slice(0, 10),
      });

      NovaGear.showToast("Account created successfully!");
      redirectAfterAuth();
    });
  }

  function redirectAfterAuth() {
    const params = new URLSearchParams(window.location.search);
    const next = params.get("next") || "profile.html";
    setTimeout(() => {
      window.location.href = next;
    }, 500);
  }

  function init() {
    if (document.body.dataset.page !== "auth") return;

    if (NovaGear.isLoggedIn()) {
      window.location.href = "profile.html";
      return;
    }

    bindTabs();
    bindLogin();
    bindRegister();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
