#!/usr/bin/env python3
"""
CARWAS M&C 173 — verificar_proyecto.py
Comprueba que todos los archivos del proyecto están en orden
antes de hacer push a GitHub.

Uso: python3 verificar_proyecto.py
"""

import os
import sys
import json

OK   = "\033[92m✅\033[0m"
WARN = "\033[93m⚠️ \033[0m"
ERR  = "\033[91m❌\033[0m"
INFO = "\033[94mℹ️ \033[0m"

errors   = 0
warnings = 0

def ok(msg):   print(f"   {OK} {msg}")
def warn(msg): global warnings; warnings += 1; print(f"   {WARN} {msg}")
def err(msg):  global errors;   errors   += 1; print(f"   {ERR} {msg}")
def info(msg): print(f"   {INFO} {msg}")
def titulo(t): print(f"\n{'─'*50}\n  {t}\n{'─'*50}")

# ── ARCHIVOS OBLIGATORIOS ──
titulo("1. Archivos obligatorios del proyecto")
OBLIGATORIOS = [
    ("index.html",                  "Landing page principal"),
    ("css/styles.css",              "Estilos CSS"),
    ("js/main.js",                  "JavaScript principal"),
    ("img/logo.png",                "Logo Carwas M&C 173"),
    ("README.md",                   "Documentación GitHub"),
    (".gitignore",                  "Git ignore"),
    ("blogger/pagina_blogger.html", "Página para Blogger"),
    ("GUIA_DESPLIEGUE.md",          "Guía de despliegue"),
    ("GUIA_BACKEND.md",             "Guía de backend"),
    ("n8n_workflow_carwas_mc.json", "Workflow n8n"),
    ("dify_agent_carwas_mc.yml",    "Agente Dify"),
    ("admin/panel_admin.html",      "Panel de administración"),
]

for path, desc in OBLIGATORIOS:
    if os.path.isfile(path):
        size = os.path.getsize(path)
        ok(f"{path} ({size:,} bytes) — {desc}")
    else:
        err(f"FALTA: {path} — {desc}")

# ── FOTOS DE GALERÍA ──
titulo("2. Fotos de galería (img/galeria1.jpg ... galeria10.jpg)")
fotos_ok = 0
for n in range(1, 11):
    path = f"img/galeria{n}.jpg"
    if os.path.isfile(path):
        size = os.path.getsize(path)
        if size > 2_000_000:
            warn(f"galeria{n}.jpg es muy grande ({size//1024} KB). Comprimí a < 800 KB.")
        else:
            ok(f"galeria{n}.jpg ({size//1024} KB)")
        fotos_ok += 1
    else:
        warn(f"galeria{n}.jpg — pendiente de agregar")

info(f"{fotos_ok}/10 fotos presentes")

# ── VERIFICAR CONTENIDO DE ARCHIVOS CLAVE ──
titulo("3. Verificación de contenido")

# index.html
if os.path.isfile("index.html"):
    with open("index.html") as f: html = f.read()
    checks = [
        ("mc-nav",         "Navbar"),
        ("mc-hero",        "Sección Hero"),
        ("mc-servicios",   "Sección Servicios"),
        ("mc-galeria",     "Sección Galería"),
        ("mc-reserva",     "Sección Reserva"),
        ("mc-contacto",    "Sección Contacto"),
        ("mcCalcularPrecio", "Calculadora de precios"),
        ("mcEnviarWA",     "Función WhatsApp"),
        ("mc-wa-float",    "Botón WA flotante"),
        ("mc-lightbox",    "Lightbox galería"),
    ]
    for key, desc in checks:
        if key in html: ok(f"index.html contiene: {desc}")
        else:           err(f"index.html NO contiene: {desc} ({key})")

    if "TU-USUARIO" in html:
        warn("index.html todavía tiene 'TU-USUARIO'. Reemplazar antes del deploy.")

# pagina_blogger.html
if os.path.isfile("blogger/pagina_blogger.html"):
    with open("blogger/pagina_blogger.html") as f: blog_html = f.read()
    if "TU-USUARIO" in blog_html:
        warn("pagina_blogger.html tiene 'TU-USUARIO'. REEMPLAZAR antes de pegar en Blogger.")
    else:
        ok("pagina_blogger.html — TU-USUARIO ya fue reemplazado")

    if "styles.css" in blog_html: ok("pagina_blogger.html enlaza CSS de GitHub Pages")
    else:                          err("pagina_blogger.html NO enlaza CSS")

# n8n workflow
if os.path.isfile("n8n_workflow_carwas_mc.json"):
    with open("n8n_workflow_carwas_mc.json") as f:
        try:
            wf = json.load(f)
            nodos = len(wf.get("nodes", []))
            ok(f"n8n workflow válido — {nodos} nodos")
            with open("n8n_workflow_carwas_mc.json") as ff: raw = ff.read()
            if "REEMPLAZAR" in raw:
                warn("n8n workflow tiene valores 'REEMPLAZAR_CON_...' — configurar antes de usar.")
        except json.JSONDecodeError:
            err("n8n_workflow_carwas_mc.json no es JSON válido")

# main.js
if os.path.isfile("js/main.js"):
    with open("js/main.js") as f: js = f.read()
    for fn in ["mcCalcularPrecio", "mcEnviarWA", "mcImgPlaceholder"]:
        if fn in js: ok(f"js/main.js contiene función: {fn}")
        else:        err(f"js/main.js NO contiene: {fn}")

# ── TAMAÑO TOTAL DEL PROYECTO ──
titulo("4. Tamaño del proyecto")
total = 0
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__']]
    for file in files:
        total += os.path.getsize(os.path.join(root, file))

info(f"Tamaño total del proyecto: {total/1024:.1f} KB")
if total > 50_000_000:
    warn("El proyecto supera 50 MB. Considerá comprimir las imágenes.")

# ── RESUMEN FINAL ──
titulo("RESUMEN FINAL")
if errors == 0 and warnings == 0:
    print(f"\n  {OK} \033[92mTodo en orden. ¡Listo para hacer push a GitHub!\033[0m\n")
elif errors == 0:
    print(f"\n  {WARN} {warnings} advertencia(s). Revisalas antes del deploy.\n")
    print("  Para hacer push igual:\n  git add . && git commit -m '🚗 Carwas M&C 173' && git push\n")
else:
    print(f"\n  {ERR} {errors} error(s) y {warnings} advertencia(s). Corregí los errores primero.\n")
    sys.exit(1)

# ── PRÓXIMOS PASOS ──
print("  PRÓXIMOS PASOS:")
print("  1. Agregar fotos galeria1.jpg ... galeria10.jpg en img/")
print("  2. Reemplazar TU-USUARIO en pagina_blogger.html")
print("  3. git add . && git commit -m '🚗 Carwas M&C' && git push")
print("  4. Activar GitHub Pages en Settings → Pages")
print("  5. Pegar pagina_blogger.html en Blogger → Nueva Página → HTML")
print()
