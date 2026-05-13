#!/bin/bash
# ╔══════════════════════════════════════════════════════════╗
# ║  CARWAS M&C 173 — setup.sh                              ║
# ║  Ejecutar UNA SOLA VEZ para inicializar el repositorio  ║
# ║                                                          ║
# ║  Uso:                                                    ║
# ║    1. Poner tus fotos en la carpeta img/                 ║
# ║    2. chmod +x setup.sh                                  ║
# ║    3. ./setup.sh TU-USUARIO-GITHUB                       ║
# ╚══════════════════════════════════════════════════════════╝

set -e

USUARIO="${1}"

if [ -z "$USUARIO" ]; then
  echo "❌ Error: Falta el usuario de GitHub."
  echo "   Uso: ./setup.sh tu-usuario-github"
  exit 1
fi

echo ""
echo "🚗 CARWAS M&C 173 — Setup del repositorio"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "👤 Usuario GitHub: $USUARIO"
echo ""

# 1. Reemplazar TU-USUARIO en todos los archivos
echo "🔄 Reemplazando TU-USUARIO con '$USUARIO'..."
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS
  sed -i '' "s/TU-USUARIO/$USUARIO/g" blogger/pagina_blogger.html
  sed -i '' "s/TU-USUARIO/$USUARIO/g" blogger/blogger_theme_inject.xml
  sed -i '' "s/TU-USUARIO/$USUARIO/g" README.md
  sed -i '' "s/TU-USUARIO/$USUARIO/g" index.html
else
  # Linux
  sed -i "s/TU-USUARIO/$USUARIO/g" blogger/pagina_blogger.html
  sed -i "s/TU-USUARIO/$USUARIO/g" blogger/blogger_theme_inject.xml
  sed -i "s/TU-USUARIO/$USUARIO/g" README.md
  sed -i "s/TU-USUARIO/$USUARIO/g" index.html
fi
echo "   ✅ Hecho"

# 2. Verificar que existen las carpetas
echo ""
echo "📁 Verificando estructura de carpetas..."
for DIR in css js img blogger; do
  if [ -d "$DIR" ]; then
    echo "   ✅ $DIR/"
  else
    mkdir -p "$DIR"
    echo "   📂 Creada: $DIR/"
  fi
done

# 3. Verificar archivos obligatorios
echo ""
echo "📄 Verificando archivos del proyecto..."
ARCHIVOS=("index.html" "css/styles.css" "js/main.js" "img/logo.png")
FALTANTES=0
for ARCHIVO in "${ARCHIVOS[@]}"; do
  if [ -f "$ARCHIVO" ]; then
    echo "   ✅ $ARCHIVO"
  else
    echo "   ❌ FALTA: $ARCHIVO"
    FALTANTES=$((FALTANTES + 1))
  fi
done

if [ $FALTANTES -gt 0 ]; then
  echo ""
  echo "⚠️  Hay $FALTANTES archivo(s) faltante(s). Agregalos antes de continuar."
fi

# 4. Verificar fotos de galería
echo ""
echo "📸 Verificando fotos de galería..."
FOTOS_OK=0
for N in $(seq 1 10); do
  if [ -f "img/galeria${N}.jpg" ]; then
    FOTOS_OK=$((FOTOS_OK + 1))
    echo "   ✅ img/galeria${N}.jpg"
  else
    echo "   ⏳ img/galeria${N}.jpg — pendiente de subir"
  fi
done
echo "   📊 $FOTOS_OK de 10 fotos presentes"

# 5. Inicializar git
echo ""
echo "🐙 Configurando Git..."
if [ ! -d ".git" ]; then
  git init
  git branch -M main
  echo "   ✅ Repositorio Git inicializado"
else
  echo "   ✅ Git ya estaba inicializado"
fi

# 6. Configurar remote
REMOTE_URL="https://github.com/${USUARIO}/carwas-mc.git"
if git remote get-url origin &>/dev/null; then
  git remote set-url origin "$REMOTE_URL"
  echo "   🔄 Remote actualizado: $REMOTE_URL"
else
  git remote add origin "$REMOTE_URL"
  echo "   ✅ Remote configurado: $REMOTE_URL"
fi

# 7. Primer commit
echo ""
echo "📦 Preparando commit inicial..."
git add .
git status --short

echo ""
read -p "¿Hacer el commit y push ahora? (s/n): " CONFIRMAR
if [[ "$CONFIRMAR" == "s" || "$CONFIRMAR" == "S" ]]; then
  git commit -m "🚗 Carwas M&C 173 — Lanzamiento inicial"
  echo ""
  echo "⬆️  Haciendo push a GitHub..."
  git push -u origin main
  echo ""
  echo "╔══════════════════════════════════════════════════════╗"
  echo "║  ✅ ¡REPOSITORIO PUBLICADO CON ÉXITO!               ║"
  echo "╚══════════════════════════════════════════════════════╝"
  echo ""
  echo "🌐 Repositorio: https://github.com/${USUARIO}/carwas-mc"
  echo "🌐 GitHub Pages: https://${USUARIO}.github.io/carwas-mc/"
  echo "   (GitHub Pages tarda 2-5 min en activarse)"
  echo ""
  echo "📋 PRÓXIMOS PASOS:"
  echo "   1. Ir a GitHub → Settings → Pages → activar branch main"
  echo "   2. Esperar 5 minutos y verificar la URL de GitHub Pages"
  echo "   3. Abrir blogger/pagina_blogger.html y copiar su contenido"
  echo "   4. En Blogger → Nueva Página → HTML → Pegar → Publicar"
else
  echo ""
  echo "ℹ️  Commit no realizado. Cuando estés listo, ejecutar:"
  echo "   git add ."
  echo "   git commit -m '🚗 Carwas M&C 173 — Lanzamiento inicial'"
  echo "   git push -u origin main"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💬 Soporte: https://wa.me/50687375227"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
