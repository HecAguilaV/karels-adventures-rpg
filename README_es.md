# Infinite Story RPG

[![Bilingual Support (English)](https://img.shields.io/badge/Language-English-purple?style=for-the-badge&logo=translate)](README.md)

---

Un motor de juego de rol (RPG) basado en texto, desarrollado como proyecto final para Code in Place 2026 de Stanford. El juego utiliza un LLM para generar capítulos e historias de forma dinámica según las decisiones del jugador y el azar de un dado.

## Características

- **Soporte bilingüe**: Puedes elegir jugar en inglés o español al iniciar. Las opciones de la consola y la narrativa de la IA se adaptarán automáticamente al idioma seleccionado. Esto se diseñó para apoyar a la comunidad de habla hispana en el aprendizaje de programación.
- **Control de estado**: Rastrea la vida (HP), el oro, el inventario y los turnos a través de un diccionario de Python que procesa las respuestas en formato JSON del modelo.
- **Tirada de dados (D20)**: Cada turno incluye el lanzamiento de un dado de 20 caras. El resultado se añade al contexto del prompt para determinar el éxito o fracaso de tus decisiones.

## Estructura

- `main.py`: Ejecuta el ciclo principal del juego.
- `data/`: Contiene los archivos JSON iniciales con los diferentes puntos de partida de las historias.
- `README.md`: Esta documentación (versión en inglés).
- `README_es.md`: Esta documentación (versión en español).

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
