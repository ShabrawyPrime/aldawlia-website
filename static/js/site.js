/* Aldawlia Group — site.js (v1.0). No dependencies. */
(function () {
  "use strict";
  var d = document, w = window, root = d.documentElement;
  var LANG = root.lang || "en";
  var reduce = w.matchMedia && w.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function qs(s, c) { return (c || d).querySelector(s); }
  function qsa(s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); }
  function store(k, v) { try { if (v === undefined) return w.localStorage.getItem(k); w.localStorage.setItem(k, v); } catch (e) { return null; } }

  /* ---------- language preference ---------- */
  qsa("[data-setlang]").forEach(function (a) {
    a.addEventListener("click", function () {
      var l = a.getAttribute("data-setlang");
      store("ag:lang", l);
      try { d.cookie = "ag_lang=" + l + ";path=/;max-age=31536000;SameSite=Lax"; } catch (e) {}
    });
  });

  /* ---------- header ---------- */
  var hdr = qs("[data-hdr]");
  function onScroll() { if (hdr) hdr.classList.toggle("is-solid", w.scrollY > 24); }
  w.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  /* mega menu */
  qsa(".has-mega").forEach(function (li) {
    var btn = qs(".mega-tg", li);
    if (!btn) return;
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = !li.classList.contains("is-open");
      li.classList.toggle("is-open", open); li.classList.remove("is-closed");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    li.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { li.classList.remove("is-open"); li.classList.add("is-closed"); btn.setAttribute("aria-expanded", "false"); btn.focus(); }
    });
    li.addEventListener("mouseleave", function () { li.classList.remove("is-closed"); });
    d.addEventListener("click", function (e) { if (!li.contains(e.target)) { li.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false"); } });
  });

  /* mobile drawer */
  var burger = qs("[data-burger]"), drawer = qs("#drawer");
  function setDrawer(open) {
    if (!drawer || !burger) return;
    drawer.hidden = !open;
    burger.setAttribute("aria-expanded", open ? "true" : "false");
    d.body.classList.toggle("no-scroll", open);
    if (hdr) hdr.classList.toggle("is-open", open);
    var useMenu = qs(".ic-menu", burger), useClose = qs(".ic-close", burger);
    if (useMenu && useClose) { useMenu.style.display = open ? "none" : ""; useClose.style.display = open ? "" : "none"; }
    if (open) { var f = qs("a", drawer); if (f) f.focus(); }
  }
  if (burger) burger.addEventListener("click", function () { setDrawer(drawer.hidden); });
  d.addEventListener("keydown", function (e) { if (e.key === "Escape" && drawer && !drawer.hidden) { setDrawer(false); burger.focus(); } });
  if (drawer) qsa("a", drawer).forEach(function (a) { a.addEventListener("click", function () { setDrawer(false); }); });

  /* ---------- hero slideshow + spectrum ---------- */
  var hero = qs("[data-hero]");
  if (hero) {
    var slides = qsa(".hero__slide", hero), dots = qsa(".dot", hero), spec = qs(".spectrum", hero);
    var cap = qs(".cap-t", hero), pp = qs("[data-pp]", hero), i = 0, timer = null, playing = !reduce;
    function show(n) {
      i = (n + slides.length) % slides.length;
      slides.forEach(function (s, k) { s.classList.toggle("is-on", k === i); s.setAttribute("aria-hidden", k === i ? "false" : "true"); });
      dots.forEach(function (b, k) { b.setAttribute("aria-current", k === i ? "true" : "false"); });
      var s = slides[i];
      if (spec) spec.style.setProperty("--pos", s.getAttribute("data-pos"));
      if (cap) cap.textContent = s.getAttribute("data-cap");
    }
    function tick() { show(i + 1); }
    function play() { clearInterval(timer); timer = setInterval(tick, 7000); playing = true; if (pp) { pp.setAttribute("aria-pressed", "false"); pp.setAttribute("aria-label", pp.getAttribute("data-l-pause")); qs(".ic-pause", pp).style.display = ""; qs(".ic-play", pp).style.display = "none"; } }
    function stop() { clearInterval(timer); playing = false; if (pp) { pp.setAttribute("aria-pressed", "true"); pp.setAttribute("aria-label", pp.getAttribute("data-l-play")); qs(".ic-pause", pp).style.display = "none"; qs(".ic-play", pp).style.display = ""; } }
    dots.forEach(function (b, k) { b.addEventListener("click", function () { show(k); if (playing) play(); }); });
    if (pp) pp.addEventListener("click", function () { playing ? stop() : play(); });
    d.addEventListener("visibilitychange", function () { if (d.hidden) clearInterval(timer); else if (playing) play(); });
    show(0); if (playing && slides.length > 1) play(); else stop();
  }

  /* ---------- industries index preview ---------- */
  qsa("[data-ix]").forEach(function (ix) {
    var pv = qs(".ix__pv", ix), img = pv && qs("img", pv);
    if (!pv || !img) return;
    qsa(".ix__row", ix).forEach(function (row) {
      function on() {
        var src = row.getAttribute("data-img");
        if (!src) { ix.classList.remove("has-pv"); return; }
        img.src = src; img.alt = row.getAttribute("data-alt") || "";
        var r = row.getBoundingClientRect(), b = ix.getBoundingClientRect(), pw = pv.offsetWidth || 300;
        pv.style.top = Math.max(0, r.top - b.top - 60) + "px";
        var rowCenter = r.left - b.left + r.width / 2;
        var x = rowCenter < b.width / 2 ? (b.width / 2 + 40) : (b.width / 2 - 40 - pw);
        pv.style.left = Math.round(x) + "px"; pv.style.right = "auto";
        ix.classList.add("has-pv");
      }
      row.addEventListener("mouseenter", on); row.addEventListener("focus", on);
      row.addEventListener("mouseleave", function () { ix.classList.remove("has-pv"); });
      row.addEventListener("blur", function () { ix.classList.remove("has-pv"); });
    });
  });

  /* ---------- map ---------- */
  var map = qs("[data-map]");
  if (map) {
    var data = {}; try { data = JSON.parse(qs("#map-data").textContent); } catch (e) {}
    var tip = qs(".map__tip", map), svg = qs("svg", map);
    function coList(cc) {
      return (data.byCountry[cc] || []).map(function (k) { var c = data.companies[k]; return '<li style="--co:' + c.color + '">' + c.name + "</li>"; }).join("");
    }
    function showTip(el, evt) {
      var cc = el.getAttribute("data-cc"); if (!cc || !data.countries) return;
      tip.innerHTML = "<strong>" + data.countries[cc] + "</strong><ul>" + coList(cc) + "</ul>";
      var mb = map.getBoundingClientRect(), x, y;
      if (evt && evt.clientX) { x = evt.clientX - mb.left; y = evt.clientY - mb.top; }
      else { var r = el.getBoundingClientRect(); x = r.left - mb.left + r.width / 2; y = r.top - mb.top + r.height / 2; }
      var tw = 230; x = Math.min(Math.max(8, x + 14), mb.width - tw - 8); y = Math.min(Math.max(8, y + 14), mb.height - 120);
      tip.style.left = x + "px"; tip.style.top = y + "px"; tip.classList.add("is-on");
    }
    function hideTip() { tip.classList.remove("is-on"); }
    qsa(".m-c.is-on", svg).forEach(function (p) {
      p.setAttribute("tabindex", "0"); p.setAttribute("role", "button");
      var cc = p.getAttribute("data-cc"); if (data.countries) p.setAttribute("aria-label", data.countries[cc]);
      p.addEventListener("mousemove", function (e) { showTip(p, e); });
      p.addEventListener("mouseleave", hideTip);
      p.addEventListener("focus", function () { showTip(p); });
      p.addEventListener("blur", hideTip);
      p.addEventListener("click", function (e) { showTip(p, e); });
    });
    var mu = qs(".mu-dot", svg);
    if (mu) { mu.addEventListener("mousemove", function (e) { showTip(mu, e); }); mu.addEventListener("mouseleave", hideTip); mu.addEventListener("focus", function () { showTip(mu); }); mu.addEventListener("blur", hideTip); }
    qsa("[data-fp]").forEach(function (btn) {
      var k = btn.getAttribute("data-fp");
      function hl(on) {
        var set = (data.markets && data.markets[k]) || [];
        qsa(".m-c.is-on", svg).forEach(function (p) {
          var inSet = set.indexOf(p.getAttribute("data-cc")) > -1;
          p.classList.toggle("is-hl", on && inSet); p.classList.toggle("is-dim", on && !inSet);
        });
        btn.classList.toggle("is-on", on);
      }
      btn.addEventListener("mouseenter", function () { hl(true); }); btn.addEventListener("mouseleave", function () { hl(false); });
      btn.addEventListener("focus", function () { hl(true); }); btn.addEventListener("blur", function () { hl(false); });
    });
  }

  /* ---------- project filters ---------- */
  var pf = qs("[data-filters]");
  if (pf) {
    var cards = qsa("[data-pcard]"), chips = qsa("[data-f]", pf), count = qs("[data-count]", pf);
    var forms = {}; try { forms = JSON.parse(count.getAttribute("data-plural")) || {}; } catch (e) {}
    var plural = null; try { plural = new Intl.PluralRules(d.documentElement.lang || "en"); } catch (e) {}
    function label(n) { var k = plural ? plural.select(n) : (n === 1 ? "one" : "other"); return (forms[k] || forms.other || "{n}").replace("{n}", n); }
    function apply(f) {
      var n = 0;
      cards.forEach(function (c) {
        var ok = f === "all" || c.getAttribute("data-cat") === f || (" " + c.getAttribute("data-cos") + " ").indexOf(" " + f + " ") > -1;
        c.hidden = !ok; if (ok) n++;
      });
      chips.forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-f") === f ? "true" : "false"); });
      if (count) count.textContent = label(n);
    }
    chips.forEach(function (b) {
      b.addEventListener("click", function () {
        var f = b.getAttribute("data-f"); apply(f);
        try { if (f === "all") history.replaceState(null, "", location.pathname); else history.replaceState(null, "", "#" + f); } catch (e) {}
      });
    });
    function fromHash() { var h = (location.hash || "").slice(1); apply(chips.some(function (b) { return b.getAttribute("data-f") === h; }) ? h : "all"); }
    fromHash(); window.addEventListener("hashchange", fromHash);
  }

  /* ---------- copy buttons ---------- */
  function copyText(text, btn) {
    function done() { if (!btn) return; var t = btn.querySelector("[data-t]"); var o = t ? t.textContent : ""; btn.classList.add("is-done"); if (t) t.textContent = btn.getAttribute("data-done") || o; setTimeout(function () { btn.classList.remove("is-done"); if (t) t.textContent = o; }, 1600); }
    function fallback() { var ta = d.createElement("textarea"); ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0"; d.body.appendChild(ta); ta.select(); try { d.execCommand("copy"); done(); } catch (e) {} d.body.removeChild(ta); }
    try { if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(text).then(done, fallback); } else fallback(); } catch (e) { fallback(); }
  }
  qsa("[data-copy]").forEach(function (b) { b.addEventListener("click", function () { copyText(b.getAttribute("data-copy"), b); }); });

  /* ---------- contact form ---------- */
  var form = qs("[data-form]");
  if (form) {
    var routes = {}; try { routes = JSON.parse(qs("#route-data").textContent); } catch (e) {}
    var need = qs("#f-need", form), routeBox = qs("[data-route]", form), ready = qs("[data-ready]", form);
    function updateRoute() {
      var r = routes.needs[need.value];
      if (!r) { routeBox.hidden = true; return; }
      var c = routes.companies[r];
      qs("[data-route-name]", routeBox).textContent = c.name;
      qs("[data-route-mail]", routeBox).textContent = c.email;
      var lg = qs("img", routeBox);
      if (c.logo) { lg.src = c.logo; lg.alt = c.name; lg.hidden = false; } else { lg.hidden = true; }
      routeBox.hidden = false;
    }
    need.addEventListener("change", updateRoute);
    function setErr(id, bad) { var f = qs("#" + id, form); var wrap = f.closest(".field") || f.closest(".check"); if (wrap) wrap.classList.toggle("is-err", bad); f.setAttribute("aria-invalid", bad ? "true" : "false"); return bad; }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var v = function (id) { return (qs("#" + id, form).value || "").trim(); };
      var bad = false, first = null;
      [["f-name", !v("f-name")], ["f-email", !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v("f-email"))], ["f-need", !v("f-need")], ["f-msg", v("f-msg").length < 5], ["f-ok", !qs("#f-ok", form).checked]].forEach(function (p) {
        if (setErr(p[0], p[1])) { bad = true; if (!first) first = p[0]; }
      });
      if (bad) { qs("#" + first, form).focus(); return; }
      var r = routes.needs[v("f-need")], c = routes.companies[r];
      var L = routes.labels;
      var body = [L.name + ": " + v("f-name"), L.company + ": " + v("f-company"), L.email + ": " + v("f-email"), L.phone + ": " + v("f-phone"), L.country + ": " + v("f-country"), L.need + ": " + qs("#f-need option:checked", form).textContent, "", v("f-msg")].join("\n");
      var subject = L.subject + " · " + qs("#f-need option:checked", form).textContent;
      var endpoint = form.getAttribute("data-endpoint");
      if (endpoint) {
        fetch(endpoint, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify({ to: c.email, subject: subject, message: body, name: v("f-name"), email: v("f-email") }) })
          .then(function (res) { if (!res.ok) throw new Error(res.status); form.innerHTML = '<div class="ready"><h3>' + L.sent + "</h3></div>"; })
          .catch(function () { showReady(); });
      } else showReady();
      function showReady() {
        qs("[data-to]", ready).textContent = c.email;
        qs("pre", ready).textContent = subject + "\n\n" + body;
        var m = qs("[data-mailto]", ready);
        m.href = "mailto:" + c.email + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
        qs("[data-copy-msg]", ready).setAttribute("data-copy", "To: " + c.email + "\nSubject: " + subject + "\n\n" + body);
        ready.hidden = false; ready.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "center" });
      }
    });
    var cm = qs("[data-copy-msg]", form); if (cm) cm.addEventListener("click", function () { copyText(cm.getAttribute("data-copy"), cm); });
    var ed = qs("[data-edit]", form); if (ed) ed.addEventListener("click", function () { ready.hidden = true; qs("#f-msg", form).focus(); });
  }

  /* ---------- brand TOC highlight ---------- */
  var toc = qs("[data-toc]");
  if (toc && "IntersectionObserver" in w) {
    var links = qsa("a", toc);
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) { links.forEach(function (a) { a.classList.toggle("is-on", a.getAttribute("href") === "#" + en.target.id); }); } });
    }, { rootMargin: "-30% 0px -60% 0px" });
    qsa(".bsec[id]").forEach(function (s) { io.observe(s); });
  }
})();
