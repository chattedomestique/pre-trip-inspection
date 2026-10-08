(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var $ = function (id) { return document.getElementById(id); };
  var root = document.documentElement;
  var SECS = DATA.secs, BYID = {}, DONE = {};
  SECS.forEach(function (s) { BYID[s.id] = s; DONE[s.id] = {}; });
  // What you have said is kept on this device, so closing the app does not lose your place.
  var STORE = 'pti-progress-v1';
  function load() {
    try {
      var o = JSON.parse(localStorage.getItem(STORE) || '{}');
      SECS.forEach(function (s) {
        var d = o[s.id];
        if (d && typeof d === 'object') Object.keys(d).forEach(function (k) { if (+k >= 0 && +k < s.items.length) DONE[s.id][k] = true; });
      });
    } catch (e) {}
  }
  function save() { try { localStorage.setItem(STORE, JSON.stringify(DONE)); } catch (e) {} }
  load();
  var mq = window.matchMedia ? matchMedia('(prefers-reduced-motion: reduce)') : null;
  var reduced = function () { return !!(mq && mq.matches); };

  // ---- the chins are islands of the opposite theme, so they always read as inverted panels
  var dark = window.matchMedia ? matchMedia('(prefers-color-scheme: dark)') : null;
  function paintChins() {
    var a = root.getAttribute('data-theme');
    var isDark = a ? a === 'dark' : !!(dark && dark.matches);
    Array.prototype.forEach.call(document.querySelectorAll('.chin'), function (c) { c.setAttribute('data-theme', isDark ? 'light' : 'dark'); });
  }
  paintChins();
  if (dark && dark.addEventListener) dark.addEventListener('change', paintChins);
  if (window.MutationObserver) new MutationObserver(paintChins).observe(root, { attributes: true, attributeFilter: ['data-theme'] });

  var bar = $('bar'), home = $('home'), run = $('run');
  function icon(n) { return '<span class="ic ic--' + n + '" aria-hidden="true"></span>'; }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }
  function plain(html) { var d = document.createElement('div'); d.innerHTML = html; return d.textContent.replace(/\s+/g, ' ').trim(); }
  function count(sid) { return Object.keys(DONE[sid]).length; }
  function nextUp() {
    for (var i = 0; i < SECS.length; i++) if (count(SECS[i].id) < SECS[i].items.length) return SECS[i];
    return null;
  }

  // ---------------------------------------------------------------- appbar
  function setBar(mode, sec) {
    if (mode === 'home') {
      bar.innerHTML = '<div class="appbar__heading"><p class="appbar__eyebrow t-meta">Forest Hills Public Schools · current as of 7/22/2026</p><h1 class="appbar__title" id="bar-t" tabindex="-1">Pre-trip inspection</h1></div>' +
        (PWA ? '<div class="appbar__end"><button class="btn" data-size="sm" type="button" id="install" hidden>Install</button></div>' : '');
      if (window.pwaSync) window.pwaSync();
    } else {
      bar.innerHTML = '<button class="btn" data-shape="circle" data-size="sm" type="button" id="bar-back" aria-label="All sections">' + icon('chevron-left') + '</button>' +
        '<div class="appbar__heading"><p class="appbar__eyebrow t-meta">Pg. ' + sec.pg + (sec.sub ? ' · ' + esc(sec.sub) : '') + '</p><h1 class="appbar__title" id="bar-t" tabindex="-1">' + esc(sec.title) + '</h1></div>' +
        '<div class="appbar__end"><button class="btn" data-shape="circle" data-size="sm" type="button" id="restart" aria-label="Start this section over">' + icon('rotate-ccw') + '</button></div>';
      $('bar-back').addEventListener('click', goHome);
      $('restart').addEventListener('click', function () { RUN && RUN.restart(); });
    }
  }

  // ---------------------------------------------------------------- home
  var homeList;
  function buildHome() {
    var nx = nextUp();
    var rows = SECS.map(function (s, k) {
      var c = count(s.id), n = s.items.length, full = c >= n;
      var meta = 'Pg. ' + s.pg + ' · ' + n + (n === 1 ? ' line' : ' lines') + (s.sub ? ' · ' + esc(s.sub) : '');
      var cur = nx && nx.id === s.id ? ' data-next="1"' : '';
      return '<li><button class="list__row" type="button" data-sec="' + s.id + '"' + cur + '>' +
        '<span class="list__main"><span class="list__title"><span class="list__idx" aria-hidden="true">' + (k + 1) + '</span><span>' + esc(s.title) + '</span></span>' +
        '<span class="list__meta">' + meta + '</span></span>' +
        '<span class="list__trail">' + (cur ? '<span class="tag">Next</span>' : '') + (full ? '<span class="ic ic--check" aria-hidden="true"></span><span class="sr-only">All said</span>' : (c ? '<span class="count">' + c + '/' + n + '</span>' : '')) + '<span class="list__chevron ic ic--chevron-right" aria-hidden="true"></span></span></button></li>';
    }).join('');
    var label = nx ? (Object.keys(DONE).some(function (k) { return count(k) > 0; }) ? 'Continue' : 'Start') : 'Start over';
    home.innerHTML = '<div class="linebox homebox" id="homebox"><ul class="list" role="list">' + rows + '</ul></div>' +
      '<section class="chin" id="homebar" aria-label="Next section"><div class="chin__head"><h2 class="t-label">' + (nx ? 'Next up' : 'All sections said') + '</h2><p class="t-meta">' + SECS.length + ' sections</p></div>' +
      '<p class="next-up">' + (nx ? esc(nx.title) : 'Nice work. Go again from the top?') + '</p>' +
      '<div class="chin__bar one"><button class="btn" data-variant="primary" type="button" id="go"><span class="btn__label">' + label + icon('arrow-right') + '</span></button></div></section>';
    paintChins();
    Array.prototype.forEach.call(home.querySelectorAll('[data-sec]'), function (b) { b.addEventListener('click', function () { openSection(b.getAttribute('data-sec')); }); });
    $('go').addEventListener('click', function () {
      if (nx) openSection(nx.id);
      else { SECS.forEach(function (s) { DONE[s.id] = {}; }); save(); buildHome(); }
    });
    var cur = home.querySelector('[data-next]'), box = $('homebox');
    if (cur) box.scrollTop = Math.max(0, cur.parentNode.offsetTop - cur.parentNode.offsetHeight);
  }
  // In an installed app the device's back button should leave a section, not the app.
  function goHome() { if (PWA && history.state && history.state.s) history.back(); else showHome(); }
  function showHome() {
    if (RUN) { RUN.destroy(); RUN = null; }
    run.hidden = true; run.innerHTML = ''; home.hidden = false;
    setBar('home'); buildHome();
  }

  // ---------------------------------------------------------------- run a section
  var RUN = null;
  function openSection(sid, fromPop) {
    var sec = BYID[sid];
    if (PWA && !fromPop) { try { history.pushState({ s: sid }, '', location.href); } catch (e) {} }
    home.hidden = true; home.innerHTML = ''; run.hidden = false;
    setBar('run', sec);
    RUN = makeRun(sec);
    var t = $('bar-t'); if (t) t.focus({ preventScroll: true });
  }

  function makeRun(sec) {
    var items = sec.items, N = items.length, done = DONE[sec.id], cur = 0, dir = 1, raf = 0;
    var used = [];
    items.forEach(function (it) { var d = it.d || sec.dia; if (used.indexOf(d) < 0) used.push(d); });
    if (used.indexOf(sec.dia) < 0) used.unshift(sec.dia);

    var rowsH = items.map(function (it, i) {
      return '<li><button class="list__row" type="button" data-row="' + i + '" data-name="' + esc(it.n) + '" tabindex="-1"><span class="list__main"><span class="list__title"><span class="list__idx" aria-hidden="true">' + esc(it.i) + '</span><span>' + esc(it.n) + '</span></span></span><span class="list__trail"><span class="done-mark" hidden><span class="ic ic--check" aria-hidden="true"></span><span class="sr-only">Said</span></span></span></button></li>';
    }).join('');
    var saysH = items.map(function (it, i) {
      var len = plain(it.t).length, tier = len <= 85 ? 'lg' : len <= 175 ? 'md' : 'sm';
      return '<p class="say s-' + tier + '" data-say="' + i + '" aria-hidden="true">' + it.t + '</p>';
    }).join('');
    run.innerHTML =
      '<section class="stage" aria-label="Part being checked"><div class="dias" id="dias">' + used.map(function (d) { return DATA.dias[d]; }).join('') + '</div>' +
      '<div class="progress" data-size="sm"><div class="progress__track"><progress class="progress__bar" id="prog-bar" value="0" max="' + N + '" aria-label="Lines said">0 of ' + N + '</progress></div></div></section>' +
      '<div class="linebox" id="linebox" role="group" aria-label="Lines in this section"><ul class="list" role="list" id="lines">' + rowsH + '</ul></div>' +
      '<section class="chin" id="chin" aria-labelledby="say-h"><div class="chin__head"><h2 class="t-label" id="say-h">You must say</h2><p class="t-meta" id="said"></p></div>' +
      '<div class="chin__say" id="says">' + saysH + '</div>' +
      '<div class="chin__bar"><button class="btn" type="button" id="back"><span class="btn__label">' + icon('arrow-left') + 'Back</span></button><button class="btn" data-variant="primary" type="button" id="next"><span class="btn__label" id="next-l">Next</span></button></div></section>' +
      '<p class="sr-only" id="live" aria-live="polite"></p>';
    run.setAttribute('data-size', N <= 4 ? 'few' : N <= 8 ? 'some' : 'many');
    $('linebox').style.maxBlockSize = 'calc(' + N + ' * 2.75rem + 2 * var(--bw))';
    paintChins();

    var rows = Array.prototype.slice.call(run.querySelectorAll('[data-row]'));
    var says = Array.prototype.slice.call(run.querySelectorAll('[data-say]'));
    var box = $('linebox'), ul = $('lines'), chin = $('chin');
    var back = $('back'), next = $('next'), nextL = $('next-l');
    var svgs = {};
    Array.prototype.forEach.call(run.querySelectorAll('.dia'), function (s, k) { svgs[used[k]] = s; });

    // which line does each part open? (the first line that names it, on that diagram)
    var link = {};
    items.forEach(function (it, i) {
      var d = it.d || sec.dia;
      it.p.forEach(function (p) { if (p === '*') return; var key = d + ':' + p; if (!(key in link)) link[key] = i; });
    });

    // hit targets (at least 22 units), drawn once per diagram
    used.forEach(function (d) {
      var svg = svgs[d], hits = svg.querySelector('.hits');
      svg.classList.add('is-shown'); // measure while laid out
      Array.prototype.forEach.call(svg.querySelectorAll('.part'), function (g) {
        var id = g.getAttribute('data-id');
        if (!((d + ':' + id) in link)) return;
        g.classList.add('is-link');
        var b = g.getBBox(), pad = 3, w = Math.max(b.width + pad * 2, 22), h = Math.max(b.height + pad * 2, 22);
        var r = document.createElementNS(NS, 'rect');
        r.setAttribute('class', 'hit'); r.setAttribute('data-id', id);
        r.setAttribute('x', b.x + b.width / 2 - w / 2); r.setAttribute('y', b.y + b.height / 2 - h / 2);
        r.setAttribute('width', w); r.setAttribute('height', h);
        hits.appendChild(r);
      });
      svg.classList.remove('is-shown');
      svg.addEventListener('click', function (e) {
        var t = e.target.closest('.hit'); if (!t) return;
        var k = link[d + ':' + t.getAttribute('data-id')];
        if (k !== undefined) go(k);
      });
    });

    function drawHalos(svg, on) {
      var h = svg.querySelector('.halos');
      while (h.firstChild) h.removeChild(h.firstChild);
      if (on['*']) return;
      Array.prototype.forEach.call(svg.querySelectorAll('.part'), function (g) {
        if (!on[g.getAttribute('data-id')] || g.getAttribute('data-halo') === 'none') return;
        Array.prototype.forEach.call(g.querySelectorAll('.p'), function (s) {
          var b = s.getBBox(), pad = 4, r = document.createElementNS(NS, 'rect');
          r.setAttribute('class', 'halo');
          r.setAttribute('x', b.x - pad); r.setAttribute('y', b.y - pad);
          r.setAttribute('width', b.width + pad * 2); r.setAttribute('height', b.height + pad * 2); r.setAttribute('rx', 4);
          h.appendChild(r);
        });
      });
    }

    // ---- the list rolls to keep the current line second from the top, eased in and out
    function rowTop(i) { return Math.round(rows[i].parentNode.getBoundingClientRect().top - ul.getBoundingClientRect().top); }
    function stride() { return rows.length > 1 ? rowTop(1) - rowTop(0) : box.clientHeight; }
    function stopMove() { if (raf) { cancelAnimationFrame(raf); raf = 0; } }
    ['touchstart', 'wheel', 'pointerdown'].forEach(function (t) { box.addEventListener(t, stopMove, { passive: true }); });
    function ease(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
    function rollTo(i, animate) {
      var max = Math.max(0, box.scrollHeight - box.clientHeight);
      var to = Math.max(0, Math.min(max, rowTop(i) - stride())), from = box.scrollTop, d = to - from, t0 = null, ms = 460;
      stopMove();
      if (!d) return;
      if (!animate || reduced()) { box.scrollTop = to; return; }
      function step(t) { if (t0 === null) t0 = t; var k = Math.min(1, (t - t0) / ms); box.scrollTop = from + d * ease(k); raf = k < 1 ? requestAnimationFrame(step) : 0; }
      raf = requestAnimationFrame(step);
    }
    box.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); go(cur + 1); rows[cur].focus({ preventScroll: true }); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); go(cur - 1); rows[cur].focus({ preventScroll: true }); }
    });

    var lastDia = null;
    function render() {
      var it = items[cur], d = it.d || sec.dia, on = {};
      it.p.forEach(function (p) { on[p] = true; });
      used.forEach(function (u) {
        var svg = svgs[u], show = u === d;
        svg.classList.toggle('is-shown', show);
        Array.prototype.forEach.call(svg.querySelectorAll('.part'), function (g) { g.classList.toggle('is-on', show && (on['*'] || !!on[g.getAttribute('data-id')])); });
        if (show) drawHalos(svg, on); else drawHalos(svg, {});
      });
      lastDia = d;
      var c = 0;
      rows.forEach(function (row, i) {
        if (i === cur) { row.setAttribute('aria-current', 'true'); row.tabIndex = 0; } else { row.removeAttribute('aria-current'); row.tabIndex = -1; }
        var dn = !!done[i]; if (dn) c++;
        row.querySelector('.done-mark').hidden = !(dn && i !== cur);
        row.querySelector('.list__title > span:last-child').classList.toggle('is-done-t', dn);
      });
      chin.style.setProperty('--dir', dir);
      says.forEach(function (s, i) {
        var was = s.classList.contains('is-on');
        s.classList.toggle('is-out', was && i !== cur);
        s.classList.toggle('is-on', i === cur);
        s.setAttribute('aria-hidden', i === cur ? 'false' : 'true');
        if (i === cur) s.classList.remove('is-out');
      });
      var txt = c + ' of ' + N;
      $('prog-bar').value = c; $('prog-bar').textContent = txt;
      $('said').textContent = txt + ' said';
      $('say-h').textContent = DATA.labels[it.l || sec.lab];
      back.disabled = cur === 0;
      nextL.textContent = cur === N - 1 ? 'Finish' : 'Next';
      $('live').textContent = it.n + ', line ' + (cur + 1) + ' of ' + N + '. ' + DATA.labels[it.l || sec.lab] + ': ' + plain(it.t);
    }

    function go(i) {
      var n = Math.max(0, Math.min(N - 1, i));
      if (n === cur) { rollTo(cur, true); return; }
      dir = n > cur ? 1 : -1;
      cur = n; render(); rollTo(cur, true);
    }
    function onNext() {
      done[cur] = true; save();
      if (cur < N - 1) go(cur + 1);
      else { render(); goHome(); }
    }
    function onBack() { go(cur - 1); }
    rows.forEach(function (row, i) { row.addEventListener('click', function () { go(i); }); });
    back.addEventListener('click', onBack);
    next.addEventListener('click', onNext);

    render();
    says[cur].style.transition = 'none'; void says[cur].offsetWidth; says[cur].style.transition = '';
    rollTo(0, false);

    return {
      restart: function () { Object.keys(done).forEach(function (k) { delete done[k]; }); save(); dir = -1; cur = 0; render(); rollTo(0, true); },
      destroy: function () { stopMove(); }
    };
  }

  if (PWA) window.addEventListener('popstate', function (e) {
    var st = e.state;
    if (st && st.s && BYID[st.s]) { if (RUN) { RUN.destroy(); RUN = null; } home.hidden = true; home.innerHTML = ''; openSection(st.s, true); }
    else showHome();
  });
  if (PWA && history.state && history.state.s && BYID[history.state.s]) openSection(history.state.s, true);
  else showHome();
})();
