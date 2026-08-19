/* QMLearn — shared header/footer + interactions */
(function () {
  "use strict";

  var page = document.body.getAttribute("data-page") || "";
  var root = document.body.getAttribute("data-root") || "";

  var navItems = [
    { id: "home",       label: "Home",       href: root + "index.html" },
    { id: "install",    label: "Install",    href: root + "install.html" },
    { id: "tutorials",  label: "Tutorials",  href: root + "tutorials.html" },
    { id: "source",     label: "The code",   href: root + "source.html" },
    { id: "contact",    label: "Contact",    href: root + "contact.html" }
  ];

  function navLinksHtml() {
    return navItems.map(function (n) {
      var active = n.id === page ? ' class="active"' : "";
      return '<li><a href="' + n.href + '"' + active + '>' + n.label + "</a></li>";
    }).join("");
  }

  var headerHtml =
    '<header class="site-header">' +
      '<div class="container nav">' +
        '<a class="brand" href="' + root + 'index.html" aria-label="QMLearn home">' +
          '<img class="brand-logo" src="' + root + '_static/qmlearn-logo.png" alt="QMLearn">' +
          '<span class="brand-text"><span>Quantum Machine Learning</span></span>' +
        '</a>' +
        '<button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false"><span></span></button>' +
        '<div class="nav-menu">' +
          '<ul class="nav-links">' + navLinksHtml() + '</ul>' +
          '<span class="nav-cta"><a class="btn btn-accent btn-sm" href="https://github.com/Quantum-MultiScale/QMLearn" target="_blank" rel="noopener">GitHub</a></span>' +
        '</div>' +
      '</div>' +
    '</header>';

  var year = new Date().getFullYear();

  var footerHtml =
    '<footer class="site-footer">' +
      '<div class="footer-top"><div class="container footer-grid">' +
        '<div class="footer-about">' +
          '<div class="footer-brand"><img class="footer-logo" src="' + root + '_static/qmlearn-logo-on-dark.png" alt="QMLearn"></div>' +
          '<p>Surrogate electronic structure methods by learning 1- and 2-electron reduced density matrices in the AO basis: energies, forces, and AIMD.</p>' +
        '</div>' +
        '<div>' +
          '<h4>Documentation</h4>' +
          '<ul class="footer-links">' +
            '<li><a href="' + root + 'install.html">Installation</a></li>' +
            '<li><a href="' + root + 'tutorials.html">Tutorials</a></li>' +
            '<li><a href="' + root + 'source.html">The code</a></li>' +
            '<li><a href="' + root + 'contact.html">Contact &amp; papers</a></li>' +
          '</ul>' +
        '</div>' +
        '<div>' +
          '<h4>Community</h4>' +
          '<ul class="footer-links">' +
            '<li><a href="https://github.com/Quantum-MultiScale/QMLearn" target="_blank" rel="noopener">GitHub repository</a></li>' +
            '<li><a href="https://www.quantum-multiscale.org/software/qmlearn.html" target="_blank" rel="noopener">Q-MS software page</a></li>' +
            '<li><a href="https://pyscf.org/" target="_blank" rel="noopener">PySCF</a></li>' +
            '<li><a href="https://wiki.fysik.dtu.dk/ase/" target="_blank" rel="noopener">ASE</a></li>' +
          '</ul>' +
        '</div>' +
      '</div></div>' +
      '<div class="sponsors"><div class="container">' +
        '<div class="label">Developed within the Quantum Multiscale collaboration</div>' +
        '<div class="sponsors-row">' +
          '<a href="https://sites.rutgers.edu/prg/" target="_blank" rel="noopener">PRG · Rutgers</a>' +
          '<a href="https://www.shaoxc.com/" target="_blank" rel="noopener">MS² Lab · Jilin</a>' +
          '<a href="https://www.quantum-multiscale.org/" target="_blank" rel="noopener">Quantum Multiscale</a>' +
        '</div>' +
      '</div></div>' +
      '<div class="footer-bottom"><div class="container" style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;width:100%">' +
        '<span>© ' + year + ' QMLearn developers.</span>' +
        '<span><a href="https://github.com/Quantum-MultiScale/QMLearn">Quantum-MultiScale/QMLearn</a></span>' +
      '</div></div>' +
    '</footer>';

  document.body.insertAdjacentHTML("afterbegin", headerHtml);
  document.body.insertAdjacentHTML("beforeend", footerHtml);

  var toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.querySelectorAll(".nav-menu a").forEach(function (a) {
      a.addEventListener("click", function () { document.body.classList.remove("nav-open"); });
    });
  }

  document.querySelectorAll(".acc-head").forEach(function (head) {
    head.addEventListener("click", function () {
      head.parentElement.classList.toggle("open");
    });
  });

  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  function copyIcon() {
    return '<svg class="copy-code-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 012-2h10"/></svg>';
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand("copy");
        resolve();
      } catch (err) {
        reject(err);
      } finally {
        document.body.removeChild(ta);
      }
    });
  }

  document.querySelectorAll("pre > code").forEach(function (code) {
      var pre = code.parentElement;
      if (!pre || (pre.parentElement && pre.parentElement.classList.contains("code-block"))) return;

      var wrap = document.createElement("div");
      wrap.className = "code-block";
      pre.parentNode.insertBefore(wrap, pre);
      wrap.appendChild(pre);

      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "copy-code-btn";
      btn.setAttribute("aria-label", "Copy code");
      btn.innerHTML = copyIcon();
      wrap.appendChild(btn);

      btn.addEventListener("click", function () {
        copyText(code.textContent || "").then(function () {
          btn.classList.add("copied");
          btn.setAttribute("aria-label", "Copied!");
          window.setTimeout(function () {
            btn.classList.remove("copied");
            btn.setAttribute("aria-label", "Copy code");
          }, 1800);
        }).catch(function () {
          btn.classList.add("failed");
          window.setTimeout(function () {
            btn.classList.remove("failed");
          }, 1800);
        });
      });
    });
})();
