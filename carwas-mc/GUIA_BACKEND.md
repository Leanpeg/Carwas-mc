# ⚙️ CARWAS M&C 173 — Guía de Configuración del Backend
## n8n + Dify + CallMeBot + Google Sheets

---

## 🗺️ ARQUITECTURA DEL SISTEMA

```
Cliente llena formulario (Blogger)
         │
         ▼
   [Webhook n8n]  ◄─────────────────────────────────┐
         │                                            │
         ▼                                            │
  [Procesar datos]                            [WhatsApp de cliente]
         │                                    (CallMeBot / Meta API)
         ▼                                            │
   [¿Datos OK?]                                       │
    ├── NO ──► Respuesta 400                          │
    └── SÍ ──► [Google Sheets] ──► [WA Cliente] ─────┘
               [WA Greivin]

Cron 7am (días hábiles):
   [Leer Sheets] ──► [Filtrar hoy] ──► [WA Recordatorio al cliente]

WhatsApp entrante (futuro):
   [WA Webhook] ──► [Dify API] ──► [Respuesta IA] ──► [WA respuesta]
```

---

## 📞 PASO 1 — CONFIGURAR CALLMEBOT (WhatsApp gratis)

CallMeBot permite enviar mensajes de WhatsApp gratis sin Meta Business.
Limitación: solo a números que hayan aceptado la invitación.

### 1.1 Registrar el número de Greivin (8737-5227):
1. Desde el WhatsApp de Greivin, enviar este mensaje a **+34 644 01 67 24**:
   ```
   I allow callmebot to send me messages
   ```
2. Recibirá su API key por respuesta (ej: `1234567`)
3. Guardar esa API key

### 1.2 Registrar el número de WhatsApp del negocio:
*(Para que los clientes también puedan recibir confirmaciones)*
- Repetir el paso anterior desde el WhatsApp de cada cliente
- Alternativa: usar **Meta WhatsApp Business API** para envío masivo (ver Paso 3)

### 1.3 Reemplazar en n8n:
En el workflow, buscar todos los campos:
```
REEMPLAZAR_CON_TU_API_KEY_CALLMEBOT
```
y reemplazar con la API key obtenida.

---

## 📊 PASO 2 — CREAR GOOGLE SHEET DE RESERVAS

### Opción A — Script automático (recomendado):
```bash
pip install google-auth google-auth-oauthlib google-api-python-client
python3 crear_sheet_reservas.py
```
El script crea la hoja con formato, validaciones y dashboard automáticamente.

### Opción B — Manual:
1. Crear nuevo Google Sheet: https://sheets.new
2. Renombrarlo: "Carwas M&C 173 — Reservas"
3. Crear 3 hojas: `Reservas`, `Dashboard`, `Configuracion`
4. En la hoja `Reservas`, agregar estos encabezados en fila 1:
   ```
   A: Timestamp
   B: Fecha_Hora_CR
   C: Nombre
   D: Telefono
   E: Direccion
   F: Vehiculo
   G: Servicio
   H: Fecha_Servicio
   I: Hora_Preferida
   J: Precio
   K: Estado
   L: Notas
   ```
5. Copiar el ID de la URL (la parte larga entre `/d/` y `/edit`)

### Obtener el ID del Sheet:
URL de ejemplo:
```
https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms/edit
                                        ↑ ESTE ES EL ID ↑
```

### Reemplazar en n8n:
Buscar en el workflow:
```
REEMPLAZAR_CON_ID_DE_TU_GOOGLE_SHEET
```
y reemplazar con tu ID real.

---

## ⚙️ PASO 3 — INSTALAR Y CONFIGURAR n8n

### Opción A — Railway.app (más fácil, casi gratis):
1. Ir a https://railway.app → "New Project"
2. Buscar template "n8n" → Deploy
3. Variables de entorno a configurar:
   ```
   N8N_BASIC_AUTH_ACTIVE=true
   N8N_BASIC_AUTH_USER=admin
   N8N_BASIC_AUTH_PASSWORD=CarwasAdmin2025!
   N8N_HOST=0.0.0.0
   N8N_PORT=5678
   WEBHOOK_URL=https://TU-PROYECTO.railway.app
   ```
4. Copiar la URL pública (ej: `https://carwas-n8n.railway.app`)

### Opción B — Render.com (gratis con limitaciones):
1. Ir a https://render.com → "New Web Service"
2. Usar imagen Docker: `n8nio/n8n:latest`
3. Configurar variables de entorno igual que Railway

### Opción C — Docker local (para pruebas):
```bash
docker run -d \
  --name carwas-n8n \
  -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=CarwasAdmin2025! \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n:latest
```
Acceder en: http://localhost:5678

### Importar el workflow:
1. Abrir n8n → menú (☰) → "Import from file"
2. Seleccionar `n8n_workflow_carwas_mc.json`
3. Configurar credenciales (ver siguiente sección)

### Credenciales a configurar en n8n:

| Servicio | Tipo | Cómo obtener |
|---------|------|-------------|
| Google Sheets | OAuth2 | n8n → Credentials → Google → OAuth2 |
| HTTP Request | Ninguna (API key en URL) | Ya incluido en los nodos |

---

## 🤖 PASO 4 — CONFIGURAR DIFY

### 4.1 Crear cuenta y app:
1. Ir a https://dify.ai → Registrarse (plan gratuito disponible)
2. "Crear aplicación" → tipo "Chatbot"
3. Nombre: `Asistente Carwas M&C 173`

### 4.2 Configurar el modelo:
1. En la app → "Modelo" → seleccionar `gpt-4o-mini`
2. Si no tenés OpenAI API key:
   - Ir a https://platform.openai.com → API Keys → Create
   - En Dify: Settings → Model Providers → OpenAI → pegar API key

### 4.3 Copiar el prompt del sistema:
1. Abrir `dify_agent_carwas_mc.yml`
2. Copiar todo el bloque debajo de `system_prompt: |`
3. En Dify: tu app → "Instrucciones del sistema" → pegar → Guardar

### 4.4 Configurar las preguntas sugeridas:
En la app → "Funciones" → "Preguntas de inicio" → agregar:
- "¿Cuánto cuesta el lavado básico para mi auto?"
- "¿Qué incluye el detallado completo?"
- "Quiero reservar para este fin de semana"
- "¿Cuáles zonas cubren?"

### 4.5 Obtener el embed para Blogger:
1. En tu app Dify → "Publicar"
2. Click en "Insertar en sitio web"
3. Copiar el código script generado
4. En Blogger → Diseño → Agregar gadget → HTML/JavaScript
5. Pegar el código → Guardar

### 4.6 Personalizar el color del botón:
Agregar al final del código embed:
```html
<style>
  #dify-chatbot-bubble-button {
    background-color: #f5c518 !important; /* Amarillo Carwas */
    bottom: 5.5rem !important; /* Arriba del botón de WhatsApp */
    right: 2rem !important;
  }
</style>
```

### 4.7 Obtener API key de Dify (para n8n):
1. En Dify → Settings → API Keys → Create new secret key
2. Copiar la key
3. En n8n, en el nodo "🤖 Llamar Agente Dify":
   ```
   REEMPLAZAR_CON_TU_DIFY_API_KEY → pegar tu key
   ```

---

## 🔗 PASO 5 — CONECTAR EL FORMULARIO WEB CON n8n

En el archivo `js/main.js`, la función `mcEnviarWA()` actualmente abre WhatsApp directamente. Para que también guarde en Google Sheets via n8n, agregar esto al final de la función (antes del `window.open`):

```javascript
// Enviar datos a n8n (registrar en Google Sheets)
const datosReserva = {
  nombre, telefono, direccion,
  vehiculo, servicio, fecha, hora
};

fetch('https://TU-N8N.railway.app/webhook/carwas-mc-reserva', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(datosReserva)
}).catch(err => console.warn('n8n no disponible:', err));
// (No bloquear si n8n falla — WhatsApp igual se abre)
```

---

## ✅ CHECKLIST COMPLETO DEL BACKEND

### CallMeBot:
- [ ] Greivin envió "I allow callmebot..." al número de CallMeBot
- [ ] API key recibida por WhatsApp
- [ ] API key reemplazada en los 3 nodos de WhatsApp del workflow n8n

### Google Sheets:
- [ ] Sheet "Carwas M&C 173 — Reservas" creada
- [ ] Hoja `Reservas` con las 12 columnas correctas
- [ ] ID del sheet copiado
- [ ] ID reemplazado en los 2 nodos de Google Sheets en n8n

### n8n:
- [ ] n8n instalado (Railway / Render / Docker)
- [ ] URL pública obtenida
- [ ] Workflow importado
- [ ] Credenciales Google Sheets configuradas
- [ ] Workflow activado (toggle verde)
- [ ] URL del webhook copiada para pegar en el JS

### Dify:
- [ ] Cuenta creada en dify.ai
- [ ] App "Asistente Carwas M&C 173" creada
- [ ] Prompt del sistema pegado
- [ ] Modelo configurado (gpt-4o-mini)
- [ ] App publicada
- [ ] Widget embed pegado en Blogger
- [ ] Color del botón personalizado (amarillo #f5c518)

### Integración final:
- [ ] URL de n8n webhook agregada al `js/main.js`
- [ ] Archivo JS actualizado en GitHub (auto-actualiza GitHub Pages)
- [ ] Prueba end-to-end: llenar formulario → verificar Sheet → WhatsApp recibido

---

## 📊 COSTOS ESTIMADOS MENSUALES

| Servicio | Plan | Costo |
|---------|------|-------|
| GitHub Pages | Free | $0 |
| Blogger | Free | $0 |
| n8n (Railway) | Hobby | ~$5/mes |
| Dify | Free (200 msgs) | $0 |
| OpenAI GPT-4o-mini | Pay as you go | ~$1-3/mes |
| CallMeBot | Free | $0 |
| Google Sheets | Free | $0 |
| **TOTAL** | | **~$5-8/mes** |

*Para escalar: Dify Pro ($59/mes) cuando supere 200 conversaciones/mes*

---

*Carwas M&C 173 · Greivin · Cartago, Costa Rica · 8737-5227 · 2025*
