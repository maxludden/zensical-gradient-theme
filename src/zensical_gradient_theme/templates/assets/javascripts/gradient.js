/*
 * Gradient theme helpers.
 *
 * Copy-to-clipboard links: any <a class="copy-install" data-copy="..."> copies
 * its data-copy text (or, without it, the link's own text) and shows a toast.
 *
 *   <a class="copy-install" data-copy="uv add my-package" href="#">uv add my-package</a>
 */
(function () {
    "use strict";

    /** Show a short-lived toast message at the bottom of the page. */
    function showToast(message) {
        var toast = document.createElement("div");
        toast.className = "gradient-toast";
        toast.setAttribute("role", "status");
        toast.textContent = message;
        document.body.appendChild(toast);
        void toast.offsetWidth; // force reflow so the transition runs
        toast.classList.add("visible");
        setTimeout(function () {
            toast.classList.remove("visible");
            toast.addEventListener("transitionend", function () {
                toast.remove();
            }, { once: true });
        }, 2000);
    }

    /** Copy text, falling back to a hidden textarea on older browsers. */
    function copyText(text) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            return navigator.clipboard.writeText(text);
        }
        return new Promise(function (resolve, reject) {
            try {
                var ta = document.createElement("textarea");
                ta.value = text;
                ta.setAttribute("readonly", "");
                ta.style.position = "fixed";
                ta.style.top = "-1000px";
                document.body.appendChild(ta);
                ta.select();
                document.execCommand("copy");
                document.body.removeChild(ta);
                resolve();
            } catch (err) {
                reject(err);
            }
        });
    }

    /** Attach click handlers to copy links not yet bound on this page. */
    function bindCopyLinks() {
        document.querySelectorAll("a.copy-install:not([data-copy-bound])").forEach(function (el) {
            el.setAttribute("data-copy-bound", "");
            el.addEventListener("click", function (ev) {
                ev.preventDefault();
                var text = (el.getAttribute("data-copy") || el.textContent || "").trim();
                if (!text) {
                    return;
                }
                copyText(text)
                    .then(function () { showToast("Copied: " + text); })
                    .catch(function () { showToast("Copy failed"); });
            });
        });
    }

    // Bind on first load and after each instant-navigation page swap.
    if (window.document$) {
        window.document$.subscribe(bindCopyLinks);
    } else {
        document.addEventListener("DOMContentLoaded", bindCopyLinks);
    }
})();
