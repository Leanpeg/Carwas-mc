/* ============================================
   CARWAS M&C 173 — main.js  v2.0
   Subir a: js/main.js en el repositorio GitHub
   ============================================ */

/* ── CONFIGURACIÓN GLOBAL ── */
const MC_CONFIG = {
  whatsapp:   '50687375227',
  n8nWebhook: '',  // Ejemplo: 'https://TU-N8N.railway.app/webhook/carwas-mc-reserva'
  negocio:    'Carwas M&C 173'
};

/* ── PRECIOS ── */
const MC_PRECIOS = {
  basico:    { auto: 5000,  suv: 7000  },
  encerado:  { auto: 7000,  suv: 10000 },
  detallado: { auto: 25000, suv: 25000 }
};
const MC_SRV = {
  basico:    'Lavado básico + aspirado',
  encerado:  'Lavado + aspirado + encerado',
  detallado: 'Detallado completo'
};
const MC_VEH = { auto: 'Automóvil 4x2', suv: 'SUV / 4x4' };

/* ════════════════════════════════════════════
   1.  NAVBAR  scroll + hamburger
════════════════════════════════════════════ */
(function () {
  const nav  = document.getElementById('mc-nav');
  const ham  = document.getElementById('mc-hamburger');
  const menu = document.getElementById('mc-nav-links');
  if (!nav) return;

  window.addEventListener('scroll', () =>
    nav.classList.toggle('scrolled', window.scrollY > 60), { passive: true });

  if (ham && menu) {
    ham.addEventListener('click', () => {
      const o = menu.classList.toggle('mc-open');
      ham.classList.toggle('active', o);
    });
    menu.querySelectorAll('a').forEach(a =>
      a.addEventListener('click', () => {
        menu.classList.remove('mc-open');
        ham.classList.remove('active');
      }));
    document.addEventListener('click', e => {
      if (!nav.contains(e.target)) {
        menu.classList.remove('mc-open');
        ham.classList.remove('active');
      }
    });
  }
})();

/* ════════════════════════════════════════════
   2.  CALCULADORA DE PRECIOS
════════════════════════════════════════════ */
function mcCalcularPrecio() {
  const v       = document.getElementById('mc-vehiculo')?.value;
  const s       = document.getElementById('mc-servicio')?.value;
  const preview = document.getElementById('mc-price-preview');
  const monto   = document.getElementById('mc-preview-amount');
  const detalle = document.getElementById('mc-preview-detail');
  if (!preview) return;

  if (v && s && MC_PRECIOS[s]?.[v]) {
    const p = MC_PRECIOS[s][v];
    monto.textContent   = '\u20a1' + p.toLocaleString('es-CR');
    detalle.textContent = MC_SRV[s] + ' \u00b7 ' + MC_VEH[v];
    preview.classList.add('visible');
  } else {
    preview.classList.remove('visible');
  }
}

/* ════════════════════════════════════════════
   3.  ENVÍO FORMULARIO  WhatsApp + n8n
════════════════════════════════════════════ */
function mcEnviarWA() {
  const get = id => (document.getElementById(id)?.value || '').trim();
  const nombre    = get('mc-nombre');
  const telefono  = get('mc-telefono');
  const direccion = get('mc-direccion');
  const vehiculo  = get('mc-vehiculo');
  const servicio  = get('mc-servicio');
  const fecha     = get('mc-fecha');
  const hora      = get('mc-hora');

  /* --- validación --- */
  const falta = [];
  if (!nombre)    falta.push('tu nombre');
  if (!direccion) falta.push('la dirección');
  if (!vehiculo)  falta.push('el tipo de vehículo');
  if (!servicio)  falta.push('el servicio');
  if (!fecha)     falta.push('la fecha deseada');
  if (falta.length) { _mcError('Por favor ingresá: ' + falta.join(', ') + '.'); return; }

  const fechaObj = new Date(fecha + 'T12:00:00');
  const manana   = new Date();
  manana.setDate(manana.getDate() + 1); manana.setHours(0,0,0,0);
  if (fechaObj < manana)         { _mcError('La fecha debe ser con al menos 24 horas de anticipación.'); return; }
  if (fechaObj.getDay() === 3)   { _mcError('Los miércoles estamos cerrados. Por favor elegí otro día 😊'); return; }

  const precio   = MC_PRECIOS[servicio]?.[vehiculo] || 0;
  const fechaFmt = fechaObj.toLocaleDateString('es-CR',
    { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

  const msg =
`\u00a1Hola Greivin! Quiero reservar con *${MC_CONFIG.negocio}* \ud83d\ude97\u2728

\ud83d\udc64 *Nombre:* ${nombre}
\ud83d\udcde *WhatsApp:* ${telefono || 'No indicado'}
\ud83d\udccd *Direcci\u00f3n:* ${direccion}
\ud83d\ude97 *Veh\u00edculo:* ${MC_VEH[vehiculo]}
\ud83e\uddf4 *Servicio:* ${MC_SRV[servicio]}
\ud83d\udcc5 *Fecha:* ${fechaFmt}
\u23f0 *Hora:* ${hora || 'Por coordinar'}
\ud83d\udcb0 *Total:* \u20a1${precio.toLocaleString('es-CR')}

\u00bfPod\u00e9s confirmar disponibilidad? \ud83d\ude0a`;

  window.open('https://wa.me/' + MC_CONFIG.whatsapp + '?text=' + encodeURIComponent(msg), '_blank');

  /* Enviar a n8n (no bloquea si falla) */
  if (MC_CONFIG.n8nWebhook) {
    fetch(MC_CONFIG.n8nWebhook, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre, telefono, direccion, vehiculo, servicio, fecha, hora })
    }).catch(() => {});
  }

  _mcExito();
}

function _mcError(msg) {
  let el = document.getElementById('mc-form-err');
  if (!el) {
    el = document.createElement('div');
    el.id = 'mc-form-err';
    el.style.cssText =
      'background:rgba(231,76,60,.12);border:1px solid rgba(231,76,60,.35);' +
      'border-radius:4px;padding:.75rem 1rem;font-size:.82rem;color:#e74c3c;margin-bottom:1rem;';
    document.querySelector('.mc-btn-wa')?.before(el);
  }
  el.textContent = '\u26a0\ufe0f ' + msg;
  el.style.display = 'block';
  setTimeout(() => { el.style.display = 'none'; }, 5000);
}

function _mcExito() {
  const btn = document.querySelector('.mc-btn-wa');
  if (!btn) return;
  const orig = btn.innerHTML;
  btn.textContent = '\u2705 \u00a1WhatsApp abierto!';
  btn.style.background = '#27ae60';
  setTimeout(() => { btn.innerHTML = orig; btn.style.background = ''; }, 3500);
}

/* ════════════════════════════════════════════
   4.  FECHA MÍNIMA + bloquear miércoles
════════════════════════════════════════════ */
(function () {
  const inp = document.getElementById('mc-fecha');
  if (!inp) return;
  const m = new Date(); m.setDate(m.getDate() + 1);
  inp.min = m.toISOString().split('T')[0];
  inp.addEventListener('change', () => {
    const d = new Date(inp.value + 'T12:00:00');
    if (d.getDay() === 3) { _mcError('Los mi\u00e9rcoles estamos cerrados. Por favor eleg\u00ed otro d\u00eda \ud83d\ude0a'); inp.value = ''; }
  });
})();

/* ════════════════════════════════════════════
   5.  LIGHTBOX
════════════════════════════════════════════ */
(function () {
  const lb    = document.getElementById('mc-lightbox');
  const lbImg = document.getElementById('mc-lightbox-img');
  if (!lb || !lbImg) return;

  document.querySelectorAll('.mc-gallery-item img').forEach(img => {
    img.style.cursor = 'zoom-in';
    img.addEventListener('click', () => {
      lbImg.src = img.src;
      lb.classList.add('active');
      document.body.style.overflow = 'hidden';
    });
  });

  const close = () => { lb.classList.remove('active'); document.body.style.overflow = ''; lbImg.src = ''; };
  lb.addEventListener('click', e => { if (e.target === lb || e.target.id === 'mc-lb-close') close(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
})();

/* ════════════════════════════════════════════
   6.  SCROLL FADE-IN
════════════════════════════════════════════ */
(function () {
  if (!('IntersectionObserver' in window)) {
    document.querySelectorAll('.mc-fade').forEach(el => el.classList.add('mc-visible'));
    return;
  }
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('mc-visible'); obs.unobserve(e.target); } });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.mc-fade').forEach(el => obs.observe(el));
})();

/* ════════════════════════════════════════════
   7.  SMOOTH SCROLL
════════════════════════════════════════════ */
(function () {
  document.querySelectorAll('a[href^="#"]').forEach(a =>
    a.addEventListener('click', e => {
      const t = document.querySelector(a.getAttribute('href'));
      if (!t) return;
      e.preventDefault();
      const off = document.getElementById('mc-nav')?.offsetHeight || 70;
      window.scrollTo({ top: t.offsetTop - off - 8, behavior: 'smooth' });
    }));
})();

/* ════════════════════════════════════════════
   8.  PLACEHOLDER de galería (global)
════════════════════════════════════════════ */
function mcImgPlaceholder(n) {
  return '<div class="mc-img-placeholder">'
    + '<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2">'
    + '<rect x="3" y="3" width="18" height="18" rx="2"/>'
    + '<circle cx="8.5" cy="8.5" r="1.5"/>'
    + '<polyline points="21 15 16 10 5 21"/>'
    + '</svg>'
    + '<span>Foto ' + n + '<br><small>img/galeria' + n + '.jpg</small></span>'
    + '</div>';
}
