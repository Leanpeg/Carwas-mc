# 🚗 CARWAS M&C 173 — GUÍA COMPLETA DE DESPLIEGUE
## GitHub → GitHub Pages → Blogger

---

## 📁 ESTRUCTURA DEL REPOSITORIO

```
carwas-mc/
├── index.html              ← Landing page (local/GitHub Pages)
├── css/
│   └── styles.css          ← Todos los estilos
├── js/
│   └── main.js             ← JavaScript (formulario, galería, etc.)
├── img/
│   ├── logo.png            ← Logo Carwas M&C 173 ✅ (ya incluido)
│   ├── galeria1.jpg        ← TUS FOTOS (ver Paso 1)
│   ├── galeria2.jpg
│   ├── galeria3.jpg
│   ├── galeria4.jpg
│   ├── galeria5.jpg
│   ├── galeria6.jpg
│   ├── galeria7.jpg
│   ├── galeria8.jpg
│   ├── galeria9.jpg
│   └── galeria10.jpg
└── blogger/
    ├── pagina_blogger.html      ← Pegar en Blogger (Página nueva)
    └── blogger_theme_inject.xml ← Pegar en Tema de Blogger (head/body)
```

---

## 📸 PASO 1 — PREPARAR Y NOMBRAR LAS FOTOS

### Requisitos de las fotos:
- **Formato:** JPG (recomendado) o PNG
- **Tamaño máximo:** 2 MB por foto (ideal < 800 KB para carga rápida)
- **Resolución recomendada:** 1200×800 px como mínimo
- **Nombres exactos:** `galeria1.jpg`, `galeria2.jpg`, ..., `galeria10.jpg`

### Cómo renombrar en tu celular (Android):
1. Abrí tu galería y seleccioná las 10 fotos
2. Compartilas a Google Drive o a tu PC
3. En la PC, renombralas: `galeria1.jpg` hasta `galeria10.jpg`

### Consejos para las fotos:
```
galeria1.jpg  → Foto principal / la mejor que tengas (TALL - se ve doble de alto)
galeria2.jpg  → Panorámica / antes-después (WIDE - se ve doble de ancho)
galeria3.jpg  → Detalle del acabado
galeria4.jpg  → Interior del auto aspirado
galeria5.jpg  → Panorámica de auto limpio (WIDE)
galeria6.jpg  → Motor o ruedas
galeria7.jpg  → Greivin trabajando
galeria8.jpg  → SUV o camioneta lavada
galeria9.jpg  → Detallado completo
galeria10.jpg → Cliente o auto en su casa
```

### Optimizar fotos (gratis, en línea):
- **https://squoosh.app** — Comprimir sin perder calidad
- **https://tinyjpg.com** — Compresión automática
- **https://imageresizer.com** — Redimensionar

---

## 🐙 PASO 2 — CREAR EL REPOSITORIO EN GITHUB

### 2.1 Crear cuenta (si no tenés):
1. Ir a **https://github.com** → "Sign up"
2. Elegir usuario (ej: `greivinmc`) — este nombre aparecerá en la URL
3. Verificar correo

### 2.2 Crear el repositorio:
1. En GitHub → botón verde **"New"**
2. Repository name: `carwas-mc`
3. Marcar ✅ **"Public"** (obligatorio para GitHub Pages gratis)
4. Click **"Create repository"**

### 2.3 Subir los archivos:

**Opción A — Desde el navegador (más fácil, sin instalar nada):**

```
1. Entrar al repositorio recién creado
2. Click "uploading an existing file" o arrastrar archivos
3. Subir los archivos en este ORDEN:

   PRIMERO — Crear la carpeta css:
   → Click "Add file" → "Create new file"
   → Escribir: css/styles.css
   → Pegar el contenido de css/styles.css
   → Click "Commit changes"

   SEGUNDO — Crear la carpeta js:
   → Click "Add file" → "Create new file"
   → Escribir: js/main.js
   → Pegar el contenido de js/main.js
   → Click "Commit changes"

   TERCERO — Subir imágenes:
   → Click "Add file" → "Upload files"
   → Arrastrar: logo.png, galeria1.jpg...galeria10.jpg
   → En el campo de destino escribir: img/
   → Click "Commit changes"

   CUARTO — Subir index.html:
   → Click "Add file" → "Upload files"
   → Seleccionar index.html
   → Click "Commit changes"
```

**Opción B — Con GitHub Desktop (recomendado a largo plazo):**
```
1. Descargar GitHub Desktop: https://desktop.github.com
2. Instalar y conectar tu cuenta
3. File → Clone Repository → seleccionar carwas-mc
4. Copiar TODOS los archivos del proyecto a la carpeta clonada
5. En GitHub Desktop: escribir mensaje "Subida inicial" → Commit → Push
```

**Opción C — Con Git en terminal:**
```bash
cd /ruta/a/carwas-mc
git init
git add .
git commit -m "Subida inicial Carwas M&C 173"
git remote add origin https://github.com/TU-USUARIO/carwas-mc.git
git branch -M main
git push -u origin main
```

---

## 🌐 PASO 3 — ACTIVAR GITHUB PAGES

1. En tu repositorio GitHub → pestaña **"Settings"**
2. En el menú izquierdo → click **"Pages"**
3. En "Source" → seleccionar **"Deploy from a branch"**
4. Branch → seleccionar **"main"** → carpeta **"/ (root)"**
5. Click **"Save"**
6. Esperar 2-3 minutos
7. Aparecerá la URL: `https://TU-USUARIO.github.io/carwas-mc/`

### ✅ Verificar que funciona:
- Abrir `https://TU-USUARIO.github.io/carwas-mc/` en el navegador
- Debería verse la landing page completa con logo y galería

---

## 📝 PASO 4 — REEMPLAZAR TU-USUARIO EN LOS ARCHIVOS

En el archivo `blogger/pagina_blogger.html`, reemplazar TODAS las ocurrencias de:
```
TU-USUARIO
```
por tu nombre de usuario real de GitHub. Ejemplo:
```
https://greivinmc.github.io/carwas-mc/css/styles.css
https://greivinmc.github.io/carwas-mc/img/logo.png
https://greivinmc.github.io/carwas-mc/img/galeria1.jpg
```

---

## 📰 PASO 5 — PUBLICAR EN BLOGGER

### Método RECOMENDADO — Nueva Página en Blogger:

1. Ir a **https://blogger.com** → tu blog
2. En el menú izquierdo → **"Páginas"** → **"Nueva página"**
3. Donde dice el título, escribir: `Carwas M&C 173`
4. En el editor, cambiar a modo **HTML** (ícono `<>` o pestaña "HTML")
5. **Borrar todo** el contenido del editor
6. Copiar y pegar el contenido completo de `blogger/pagina_blogger.html`
7. Click **"Publicar"**
8. Click **"Ver página"** para verificar

### Hacer que sea la página de inicio:
1. En Blogger → **"Configuración"**
2. Buscar **"Página de inicio"** → seleccionar tu nueva página
3. Guardar

---

## 🎨 PASO 6 — PERSONALIZAR PARA BLOGGER (OPCIONAL)

### Inyectar CSS/JS en el tema de Blogger:
*(Solo si querés que el estilo aplique en todas las páginas del blog)*

1. Ir a **"Tema"** → **"Editar HTML"**
2. Buscar `</head>` con Ctrl+F
3. Pegar ANTES de `</head>`:
```html
<link rel='preconnect' href='https://fonts.googleapis.com'/>
<link href='https://fonts.googleapis.com/css2?family=Bebas+Neue&amp;family=DM+Sans:wght@300;400;500;600;700&amp;display=swap' rel='stylesheet'/>
<link rel='stylesheet' href='https://TU-USUARIO.github.io/carwas-mc/css/styles.css'/>
```
4. Buscar `</body>`
5. Pegar ANTES de `</body>`:
```html
<script src='https://TU-USUARIO.github.io/carwas-mc/js/main.js' defer='defer'></script>
```

---

## 🔄 PASO 7 — CÓMO ACTUALIZAR LAS FOTOS DESPUÉS

### Opción A — Reemplazar en GitHub (desde navegador):
1. Ir a tu repositorio → carpeta `img/`
2. Click en la foto a reemplazar (ej: `galeria1.jpg`)
3. Click el ícono de lápiz ✏️ → "Replace file"
4. Subir la nueva foto con el **mismo nombre exacto**
5. "Commit changes"
6. Esperar ~2 min → GitHub Pages se actualiza automáticamente

### Opción B — Subir nueva foto con otro nombre:
1. Subir `galeria1_nueva.jpg` a la carpeta `img/`
2. En `pagina_blogger.html` cambiar:
   ```html
   src="https://TU-USUARIO.github.io/carwas-mc/img/galeria1.jpg"
   ```
   por:
   ```html
   src="https://TU-USUARIO.github.io/carwas-mc/img/galeria1_nueva.jpg"
   ```
3. Guardar y volver a pegar en Blogger

---

## 🔧 PASO 8 — SOLUCIÓN DE PROBLEMAS COMUNES

### Problema: Las imágenes no aparecen en Blogger
**Solución:**
- Verificar que GitHub Pages esté activo (Settings → Pages)
- Esperar 5 min después de subir imágenes
- Verificar que el nombre del archivo sea exactamente igual (distingue mayúsculas)
- Probar la URL directamente: `https://TU-USUARIO.github.io/carwas-mc/img/galeria1.jpg`

### Problema: El CSS no carga en Blogger
**Solución:**
- Blogger bloquea algunas URLs externas → ir a "Configuración → Básico → Habilitar HTTPS"
- Asegurarse que la URL sea `https://` (no `http://`)
- Esperar hasta 10 min para que GitHub Pages se propague

### Problema: El menú hamburger no funciona en móvil
**Solución:**
- Verificar que el JS esté cargando correctamente
- Abrir las Herramientas de Desarrollador (F12) → Console → buscar errores en rojo

### Problema: El formulario no abre WhatsApp
**Solución:**
- En Android, verificar que WhatsApp esté instalado
- En el JS, el número es `50687375227` (código Costa Rica + número)
- Probar directamente: `https://wa.me/50687375227`

---

## ✅ CHECKLIST DE LANZAMIENTO

**GitHub:**
- [ ] Repositorio `carwas-mc` creado en GitHub (público)
- [ ] Carpeta `css/` con `styles.css` subida
- [ ] Carpeta `js/` con `main.js` subida
- [ ] Carpeta `img/` con `logo.png` subida
- [ ] Fotos de galería `galeria1.jpg` ... `galeria10.jpg` subidas
- [ ] `index.html` subido
- [ ] GitHub Pages activado → URL funcionando

**Blogger:**
- [ ] `TU-USUARIO` reemplazado en `pagina_blogger.html`
- [ ] Página nueva creada en Blogger con el contenido HTML
- [ ] Página publicada y visible
- [ ] Navegación funcionando (links del menú)
- [ ] Formulario probado → abre WhatsApp con datos
- [ ] Galería probada → fotos cargando y lightbox funcionando
- [ ] Vista móvil probada → menú hamburger y formulario responsive

**Post-lanzamiento:**
- [ ] Compartir URL en estado de WhatsApp
- [ ] Publicar en Facebook con foto del logo
- [ ] Publicar en Instagram con foto del servicio
- [ ] Pedirles a clientes satisfechos que compartan

---

## 📊 URLs FINALES DEL PROYECTO

| Recurso | URL |
|---------|-----|
| Repositorio GitHub | `https://github.com/TU-USUARIO/carwas-mc` |
| GitHub Pages (landing) | `https://TU-USUARIO.github.io/carwas-mc/` |
| CSS | `https://TU-USUARIO.github.io/carwas-mc/css/styles.css` |
| JS | `https://TU-USUARIO.github.io/carwas-mc/js/main.js` |
| Logo | `https://TU-USUARIO.github.io/carwas-mc/img/logo.png` |
| Blogger | `https://TU-BLOG.blogspot.com/p/carwas-mc.html` |
| WhatsApp directo | `https://wa.me/50687375227` |

---

*Carwas M&C 173 · Greivin · Cartago, Costa Rica · 8737-5227 · © 2025*
