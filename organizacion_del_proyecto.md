# Framework #
Conjunto de clases necesarias para desarrollar una nueva aplicación.

# Editor de sprites #
**GUI**: interfaz sugar (por ahora) del editor

**Logica**: funcionalidades de cargar, guardar, editar los sprites.

# Game Editor #
**Formato del proyecto**: información que contiene el XML (por ahora), que es suficiente para describir en su totalidad un juego. Se tiene en consideración datos propios del entorno OLPC (a saber: internacionalización, bundle, etc.)

**Compilador**: basado en un XML que describe el juego y el framework:
  * genera una vista rápida del frame actual de juego (sin generar el archivo XO)
  * se genera el código necesario para integrar las clases del framework y arma el archivo XO para distribución.

**GUI**: interfaz (tecnología a definir) que permite generar de forma amigable un proyecto de juego (guardarlo/cargarlo) y crear una aplicación funcional del mismo (compilarlo)