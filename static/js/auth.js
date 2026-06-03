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
     } else {
        switchTab("login");
    }
  }

  function bindLogin() {
    document.querySelector("[data-login-form]")?.addEventListener("submit", (e) => {
      const form = e.target;

      if (!form.email.value.trim() || !form.password.value.trim()) {
        e.preventDefault();
        NovaGear.showToast("Please fill in all fields");
      }
    });
  }

  function bindRegister() {
    document.querySelector("[data-register-form]")?.addEventListener("submit", (e) => {
      const form = e.target;

      const name = form.displayName.value.trim();
      const password = form.password.value;
      const confirm = form.passwordConfirm.value;

      if (!name) {
        e.preventDefault();
        NovaGear.showToast("Please enter a display name");
        return;
      }

      if (password.length < 6) {
        e.preventDefault();
        NovaGear.showToast("Password must be at least 6 characters");
        return;
      }

      if (password !== confirm) {
        e.preventDefault();
        NovaGear.showToast("Passwords do not match");
        return;
      }

      // если всё прошло успешно —
      // форма отправится в Django обычным способом
    });
  }


  function init() {
    if (document.body.dataset.page !== "auth") return;

    bindTabs();
    bindLogin();
    bindRegister();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
