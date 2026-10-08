/* Offline app shell. build.py replaces the version below with a hash of the files, so every change to the app
   installs a new worker and drops the old cache. */
const VERSION = '__VERSION__'
const SHELL = `shell-${VERSION}`
const PRECACHE = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable-192.png',
  './icons/icon-maskable-512.png',
  './icons/apple-touch-icon-180.png',
]
self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(SHELL)
    // cache: 'reload' skips the HTTP cache, so a host that sends max-age cannot hand the worker stale files
    await cache.addAll(PRECACHE.map((url) => new Request(url, { cache: 'reload' })))
    // No skipWaiting() here: the page offers the update and waits to be asked.
  })())
})
self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    for (const key of await caches.keys()) if (key.startsWith('shell-') && key !== SHELL) await caches.delete(key)
    await self.clients.claim()
  })())
})
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') self.skipWaiting()
})
self.addEventListener('fetch', (event) => {
  const req = event.request
  if (req.method !== 'GET') return
  const url = new URL(req.url)
  if (url.origin !== self.location.origin) return
  event.respondWith((async () => {
    const shell = await caches.open(SHELL)
    if (req.mode === 'navigate') {
      return (await shell.match(req, { ignoreSearch: true })) || (await shell.match('./index.html')) || fetch(req)
    }
    return (await shell.match(req)) || fetch(req)
  })())
})
