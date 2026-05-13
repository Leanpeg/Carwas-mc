/* ================================================
   CARWAS M&C 173 — Service Worker (sw.js)
   Cache offline básico para la landing page
   ================================================ */

const CACHE_NAME   = 'carwas-mc-v1';
const CACHE_STATIC = [
  '/',
  '/index.html',
  '/css/styles.css',
  '/js/main.js',
  '/img/logo.png',
  'https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600;700&display=swap'
];

/* ── Instalar: cachear archivos estáticos ── */
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(CACHE_STATIC);
    }).then(() => self.skipWaiting())
  );
});

/* ── Activar: limpiar caches viejos ── */
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      )
    ).then(() => self.clients.claim())
  );
});

/* ── Fetch: cache-first para estáticos, network-first para el resto ── */
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Solo manejar GET
  if (event.request.method !== 'GET') return;

  // No interceptar llamadas a WhatsApp, n8n o APIs externas
  if (url.hostname === 'wa.me' ||
      url.hostname.includes('n8n') ||
      url.hostname.includes('dify') ||
      url.hostname.includes('callmebot')) return;

  // Estáticos: cache-first
  if (
    url.pathname.endsWith('.css') ||
    url.pathname.endsWith('.js') ||
    url.pathname.endsWith('.png') ||
    url.pathname.endsWith('.jpg') ||
    url.pathname.endsWith('.webp') ||
    url.hostname === 'fonts.googleapis.com' ||
    url.hostname === 'fonts.gstatic.com'
  ) {
    event.respondWith(
      caches.match(event.request).then(cached => {
        return cached || fetch(event.request).then(response => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          return response;
        });
      })
    );
    return;
  }

  // HTML: network-first, fallback al cache
  event.respondWith(
    fetch(event.request)
      .then(response => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});
