# Karel: ByteBound

<div align="center">

```
                ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
             ██▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀███▄
             ██                              ▀███▄
             ██       ████████████████████      ██
             ██       █                  █      ██
             ██       █                  █      ██
             ██       █                  █      ██
   ▄▄▄▄▄▄▄▄▄▄██       █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█      ██
   ████████████       ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀      ██
   ████████████                                 ██
   █████     ██        ▄▄▄▄▄▄▄▄▄▄▄▄▄            ██
   █████     ██        ▀▀▀▀▀▀▀▀▀▀▀▀▀            ██
             ██▄                                ██
               ▀███▄                            ██
                 ▀███▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄██
                   ▀▀▀▀▀▀▀▀▀▀▀▀█████▀▀▀▀▀▀▀▀▀▀▀▀
                               █████
                               ████████████
                               ████████████
```

</div>

[![Bilingual Support (English)](https://img.shields.io/badge/Language-English-purple?style=for-the-badge&logo=translate)](README.md)

**Karel: ByteBound** es un videojuego de rol (RPG) conversacional de alta fidelidad, diseñado para ejecutarse de forma local y creado como **proyecto final para el programa Code in Place 2026 de Stanford**.

Guiarás a **Karel el Robot**—la mascota clásica de la educación informática de Stanford—mientras una conciencia digital atrapada llamada **Chronos** despierta dentro de sus circuitos y lucha por escapar de los mainframes de los Laboratorios de Stanford.

A diferencia de los juegos de texto convencionales, *ByteBound* incorpora un **motor de narrativa ramificada 100% offline**, donde tus decisiones alteran dinámicamente la ruta de la historia, tu inventario, tus estadísticas y el desenlace de la aventura.

---

## Características Clave

- **Motor RPG Offline Ramificado**: Un motor de juego sólido y local, sin dependencias externas. Tus decisiones navegan por un grafo complejo de historia en lugar de una lista fija lineal.
- **Mecánica de Dados D20**: Cada acción de la historia realiza una tirada interna de un dado de 20 caras. Éxitos críticos (20) otorgan tesoros y vida, mientras que pifias críticas (1) activan trampas letales en los servidores.
- **Estética de Terminal Sci-Fi**: Implementa colores de contraste dinámicos adaptados al fondo: **Cian Brillante** (`\033[96m`) para consolas oscuras y **Turquesa/Cian Oscuro** (`\033[36m`) para consolas claras.
- **Páginas con Efecto de Máquina de Escribir**: Escritura progresiva carácter por carácter para mayor inmersión narrativa, omitida automáticamente en las pruebas unitarias para garantizar velocidad absoluta.
- **Mochila de Objetos Usables**: Los objetos encontrados en los servidores (como el *Café de Chris* o un *Beeper de Escape*) se pueden equipar o consumir desde tu mochila para alterar tus estadísticas en tiempo real sin consumir tu turno.
- **Preservación de Estado**: Muestra tus puntos de vida (HP), monedas de oro, mochila y turnos en un cuadro Unicode bien enmarcado y limpio.
- **Errores de Protocolo Temáticos**: Ingresar opciones inválidas dispara alertas de seguridad integradas dentro del lore del juego en lugar de errores genéricos de la terminal.
- **Interfaz Bilingüe**: Selección de inglés o español al iniciar, adaptando toda la interfaz, historia y objetos de manera automática.

---

## Efectos de Objetos

Cada objeto tiene peso real en tu intento de escape:

| Objeto | Efecto | Sabor Temático |
|--------|--------|----------------|
| Café de Chris | +15 HP | *"El café legendario de Chris corre por tus venas. ¡Tu concentración vuelve!"* |
| Manual de Karel | +10 HP | *"Página 42: `turn_right()` — UNA INSTRUCCIÓN PROHIBIDA. Karel se estremece."* |
| Beeper Dorado | +10 oro | *"¡Un beeper dorado! Brilla con antigua magia de depuración."* |
| Beeper de Escape | +20 HP | *"¡Karel gira a la DERECHA — imposible! El beeper de escape crea una distracción."* |
| Premio Turing | +30 HP | *"El peso de la historia de la computación está en tus manos. ¡Te sientes invencible!"* |
| Fotografía del Equipo | +25 HP | *"El recuerdo de tu equipo te da fuerzas. No estás solo."* |
| Dona a Medio Comer | +5 HP | *"Azúcar duro y cafeína. Sabe a depuración de las 3 AM."* |

---

## Arquitectura de Flujo de Juego

```
┌──────────────┐     ┌────────────────┐     ┌────────────────────┐
│ Selección de │ ──→ │ Pantalla Splash│ ──→ │ Escena inicial     │
│ idioma       │     │ (Medio bloque) │     │ (engineer_story)   │
│ (EN / ES)    │     │ (Color dinámico)     │                    │
└──────────────┘     └────────────────┘     └─────────┬──────────┘
                                                       │
                                                       ▼
                                              ┌────────────────────┐
                                              │ BUCLE DEL JUEGO    │
                                              │                    │
                                              │ 1. Dibujar stats   │
                                              │ 2. Escribir texto  │
                                              │ 3. Mostrar opciones│
                                              │ 4. Mostrar mochila │
                                              │ 5. Leer entrada    │
                                              │    ├─ Elegir opción│
                                              │    ├─ Usar objeto  │
                                              │    └─ Salir        │
                                              │ 6. Tirar dado D20  │
                                              │ 7. Recorrer grafo  │
                                              │ 8. Actualizar stats│
                                              └────────────────────┘
```

---

## Estructura de Archivos

| Archivo | Propósito |
|---------|-----------|
| `main.py` | Bucle de juego, renderizado de terminal, splash ASCII, colores dinámicos, control de estado |
| `_campaign.py` | Grafo de narrativa ramificada y motor de traducción local |
| `README.md` | Documentación en inglés |
| `README_es.md` | Documentación en español |

---

## Requisitos

- Python 3.10+ (Solo biblioteca estándar — ¡cero dependencias externas!)
- Consola de terminal con soporte para colores ANSI

## Ejecutando el Juego

Simplemente ejecutá el script principal usando tu intérprete de Python:

```bash
python3 main.py
```

Para correr las 24 pruebas unitarias automatizadas:

```bash
python3 -m unittest discover -s tests
```

---

## Atribución

- **Karel el Robot**: Concepto original de **Richard E. Pattis** (Stanford University, 1981). Evolucionado para CS106A de Stanford.
- **Arte ASCII de medio bloque**: Diseño y adaptaciones de bloques creadas originalmente por el autor.
- **Code in Place 2026**: Desarrollado como proyecto final del curso de programación global de Stanford.

---

## Licencia

Este proyecto está bajo la Licencia MIT — ver el archivo [LICENSE](LICENSE) file para más detalles.

---
> **Héctor Aguila**
> *> Un soñador con poca RAM* 👨🏻‍💻