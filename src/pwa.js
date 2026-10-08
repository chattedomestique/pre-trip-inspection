(function () {
  'use strict';
  // ---- install: Chrome and Edge offer a prompt; on an iPhone use Share, then Add to Home Screen
  var deferred = null;
  function standalone() { return (window.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone === true; }
  window.pwaSync = function () { var b = document.getElementById('install'); if (b) b.hidden = !deferred || standalone(); };
  window.addEventListener('beforeinstallprompt', function (e) { e.preventDefault(); deferred = e; window.pwaSync(); });
  window.addEventListener('appinstalled', function () { deferred = null; window.pwaSync(); });
  document.addEventListener('click', function (e) {
    if (!(e.target.closest && e.target.closest('#install')) || !deferred) return;
    var d = deferred; deferred = null; window.pwaSync(); d.prompt();
  });

  // ---- offline: a service worker keeps the whole app on the device
  if (!('serviceWorker' in navigator) || !/^https?:$/.test(location.protocol)) return;
  var banner = document.getElementById('update'), go = document.getElementById('update-go');
  function offer(w) {
    banner.hidden = false;
    go.onclick = function () { go.disabled = true; w.postMessage({ type: 'SKIP_WAITING' }); };
  }
  navigator.serviceWorker.register('sw.js', { scope: './', updateViaCache: 'none' }).then(function (reg) {
    if (reg.waiting && navigator.serviceWorker.controller) offer(reg.waiting);
    reg.addEventListener('updatefound', function () {
      var w = reg.installing;
      w.addEventListener('statechange', function () { if (w.state === 'installed' && navigator.serviceWorker.controller) offer(w); });
    });
    // An installed app is rarely started cold: look for a new version whenever it comes back to the front.
    document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'visible') reg.update().catch(function () {}); });
  }).catch(function () {});
  // The first visit also changes controller (the worker takes over); only reload for an update after that.
  var had = !!navigator.serviceWorker.controller, reloading = false;
  navigator.serviceWorker.addEventListener('controllerchange', function () {
    if (!had) { had = true; return; }
    if (reloading) return;
    reloading = true; location.reload();
  });
})();
