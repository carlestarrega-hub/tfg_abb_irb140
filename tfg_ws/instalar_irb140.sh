#!/bin/bash
echo "🚧 Iniciando reconstrucción manual del ABB IRB 140..."

# 1. Crear estructura de carpetas limpia
BASE_DIR=~/tfg_ws/src/abb_irb140_support
mkdir -p $BASE_DIR/urdf
mkdir -p $BASE_DIR/meshes/irb140/visual
mkdir -p $BASE_DIR/meshes/irb140/collision
mkdir -p $BASE_DIR/launch
mkdir -p $BASE_DIR/config

# 2. Descargar los archivos de Lógica (URDF/XACRO)
echo "⬇️ Descargando cinemática..."
URL_BASE="https://raw.githubusercontent.com/ros-industrial/abb_experimental/kinetic-devel/abb_irb140_support"

wget -q $URL_BASE/urdf/irb140.xacro -O $BASE_DIR/urdf/irb140.xacro
wget -q $URL_BASE/urdf/irb140_macro.xacro -O $BASE_DIR/urdf/irb140_macro.xacro
# Descargar materiales comunes (colores)
wget -q https://raw.githubusercontent.com/ros-industrial/abb/kinetic-devel/abb_resources/urdf/common_materials.xacro -O $BASE_DIR/urdf/common_materials.xacro

# 3. Descargar las Piezas 3D (Meshes) una a una
echo "⬇️ Descargando piezas 3D (Esto puede tardar un poco)..."
MESH_URL="$URL_BASE/meshes/irb140"

# Lista de piezas visuales
for file in base_link.stl link_1.stl link_2.stl link_3.stl link_4.stl link_5.stl link_6.stl; do
    wget -q $MESH_URL/visual/$file -O $BASE_DIR/meshes/irb140/visual/$file
    echo "  - Visual: $file"
done

# Lista de piezas de colisión
for file in base_link.stl link_1.stl link_2.stl link_3.stl link_4.stl link_5.stl link_6.stl; do
    wget -q $MESH_URL/collision/$file -O $BASE_DIR/meshes/irb140/collision/$file
    echo "  - Colisión: $file"
done

# 4. Ajuste de rutas (Parche para que funcione en tu carpeta)
# El archivo original busca 'abb_resources', nosotros lo hemos bajado local. Ajustamos la ruta.
sed -i 's|package://abb_resources/urdf/common_materials.xacro|package://abb_irb140_support/urdf/common_materials.xacro|g' $BASE_DIR/urdf/irb140_macro.xacro

echo "✅ ¡Robot reconstruido correctamente!"
