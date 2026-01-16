cmake_minimum_required(VERSION 3.8)
project(abb_irb140_support)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Dependencias del paquete
find_package(ament_cmake REQUIRED)
find_package(urdf REQUIRED)
find_package(xacro REQUIRED)

# ---------------------------------------------------------
# SECCIÓN DE INSTALACIÓN
# Aquí le decimos a ROS 2 qué carpetas copiar al sistema.
# Hemos añadido 'meshes' para que encuentre las pieles del robot.
# ---------------------------------------------------------
install(DIRECTORY launch urdf meshes
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
