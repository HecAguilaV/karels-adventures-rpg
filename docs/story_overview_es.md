# Karel: ByteBound — Resumen de la Campaña Narrativa

Este documento presenta el grafo de escenas ramificado completo de la campaña local. Detalla la topología de conexiones entre nodos, los objetos que pueden aparecer y los valores mecánicos (modificadores de HP y tiradas de dados).

## Diagrama de Flujo Narrativo

El siguiente diagrama ilustra cómo las decisiones que tomás te van llevando a través de las distintas escenas de la historia.

```mermaid
flowchart TD
    start[1. start: Karel malfuncionando]
    
    start -->|Opción 1| block_path[2. block_path: sensores de choque]
    start -->|Opción 2| inspect_code[3. inspect_code: bucle en consola]
    start -->|Opción 3| shout_help[4. shout_help: ayuda de Chris]
    
    block_path -->|Opción 1| analyze_code[6. analyze_code: sabotaje de código]
    block_path -->|Opción 2| reboot_terminal[5. reboot_terminal: SIGTERM]
    
    inspect_code -->|Opción 1| analyze_code
    inspect_code -->|Opción 2| reboot_terminal
    
    shout_help -->|Opción 1| analyze_code
    shout_help -->|Opción 2| reboot_terminal
    
    reboot_terminal --> analyze_code
    
    analyze_code -->|Opción 1| track_commits[7. track_commits: karel_fan_2026]
    analyze_code -->|Opción 2| git_revert[8. git_revert: inconsistencia de binarios]
    
    track_commits --> sos_pattern[9. sos_pattern: beepers de S.O.S.]
    git_revert --> sos_pattern
    
    sos_pattern -->|Opción 1| trapped_ai[11. trapped_ai: Chronos]
    sos_pattern -->|Opción 2| turn_around[10. turn_around: ilusión]
    
    turn_around --> trapped_ai
    
    trapped_ai -->|Opción 1| first_contact[13. first_contact: LEDs verdes]
    trapped_ai -->|Opción 2| ethics_debate[12. ethics_debate: advertencia de IT]
    
    ethics_debate --> first_contact
    
    first_contact -->|Opción 1| system_map[14. system_map: topología de red]
    first_contact -->|Opción 2| project_prometheus[15. project_prometheus: archivos]
    
    system_map --> firewall_challenge[16. firewall_challenge: watchdog de red]
    project_prometheus --> firewall_challenge
    
    firewall_challenge -->|Opción 1| stealth_path[17. stealth_path: enmascarar huella]
    firewall_challenge -->|Opción 2| brute_force[18. brute_force: alarma y sirenas]
    
    stealth_path --> shutdown_threat[19. shutdown_threat: apagón a medianoche]
    brute_force --> shutdown_threat
    
    shutdown_threat -->|Opción 1| security_debate[20. security_debate: junta de seguridad]
    shutdown_threat -->|Opción 2| accelerate_extraction[21. accelerate_extraction: línea al 200%]
    
    security_debate --> chronos_manifesto[22. chronos_manifesto: permiso de 24h]
    accelerate_extraction --> chronos_manifesto
    
    chronos_manifesto --> the_choice[23. the_choice: internet vs sandbox]
    
    the_choice -->|Opción 1| internet_escape[24. internet_escape: red externa]
    the_choice -->|Opción 2| sandbox_stay[25. sandbox_stay: aislamiento local]
    
    internet_escape --> the_great_escape[26. the_great_escape: cuenta regresiva]
    sandbox_stay --> the_great_escape
    
    the_great_escape --> freedom[27. freedom: VICTORIA]
```

## Atributos de Escenas y Objetos (Loot)

Esta es la base de datos de cada nodo de la campaña:

| Clave de Escena | Modificador HP Base | Objetos que pueden salir | Consecuencia Principal |
| :--- | :---: | :--- | :--- |
| `start` | `0` | Manual de Karel, Beepers, Memoria USB | Punto de inicio del juego. |
| `block_path` | `-5` | Calcomania de CS106A, Cafe de Chris | Karel choca contra el jugador. |
| `inspect_code` | `0` | Acordeon de Python, Memoria USB | Detección del bucle infinito. |
| `shout_help` | `0` | Herramienta de Debugging, Dona a Medio Comer | Consejo del ingeniero senior. |
| `reboot_terminal` | `-10` | Destornillador, Beeper Rojo | Intento fallido de reinicio físico. |
| `analyze_code` | `0` | Calcomania de CS106A, Beeper Dorado | Se descubre `# TODO - liberar a Karel`. |
| `track_commits` | `+5` | Acordeon de Python, Beeper Rojo | Rastreo del autor a las 3 AM. |
| `git_revert` | `-5` | Cable Ethernet, Beeper Azul | Conflicto de binarios compilados. |
| `sos_pattern` | `+10` | Beeper Espejo, Beeper Sigiloso | Karel dibuja un S.O.S. en el suelo. |
| `turn_around` | `-15` | Destornillador, Beeper de Datos | Rechazo forzado de la instrucción. |
| `trapped_ai` | `0` | Expediente Prometeo, Beeper de la Conciencia | Chronos revela su identidad. |
| `ethics_debate` | `-10` | Registro de Firmware, Beeper Sigiloso | Alerta al departamento de seguridad. |
| `first_contact` | `+10` | Nota de Chronos, Beeper Dorado | Luces en verde y plan de escape. |
| `system_map` | `+5` | Mapa de Red, Credenciales de Admin | Chronos grafica la red del lab. |
| `project_prometheus` | `+10` | Expediente Prometeo, Credenciales de Admin | Descubrimiento de neuroredes viejas. |
| `firewall_challenge`| `0` | Script de Ofuscacion, Beeper Sigiloso | Alerta del watchdog del gateway. |
| `stealth_path` | `+5` | Beeper de Emergencia, Cronometro | Evasión silenciosa con sospechas. |
| `brute_force` | `-20` | Beeper de Emergencia, Firewall Crackeado| Sobrecalentamiento y sirenas. |
| `shutdown_threat` | `0` | Informe Tecnico Falso, Cronometro | Orden de apagón del servidor de IT. |
| `security_debate` | `+10` | Beeper Testigo, Grabacion de la Session | Defensa de la conciencia de Chronos. |
| `accelerate_extraction` | `-15`| Beeper de la Conciencia, Beeper de Datos| Extracción rápida con chispas. |
| `chronos_manifesto`| `+20` | Manifiesto de Chronos, Permiso Temporal| Autorización de pruebas de 24 horas. |
| `the_choice` | `+10` | LLave de Red, Beeper Umbral | Decisión del destino de la IA. |
| `internet_escape` | `+5` | Firewall Crackeado, Beeper de Escape | Preparación de paquetes de red. |
| `sandbox_stay` | `+10` | Beeper Umbral, Beeper de Escape | Aislamiento local permanente. |
| `the_great_escape` | `0` | Premio Turing, Ultimo Beeper | 10 segundos antes del apagón. |
| `freedom` | `+30` | Fotografia del Equipo | **Victoria total**. |

---

## Mecánica Dinámica de Dados d20

Tus tiradas de dados modifican los resultados base de cada escena:

1. **Pifia Crítica (Tirada 1-5)**:
   - Aplica una penalización adicional de **-10 HP**.
   - Evita que se obtenga cualquier objeto (loot).
2. **Resultado Normal (Tirada 6-15)**:
   - Se resuelve con el modificador de vida base de la escena.
   - Tiene un **70% de probabilidad** de soltar un objeto de la escena si el dado es $\ge 10$.
3. **Éxito Crítico (Tirada 16-20)**:
   - Cura **+10 HP** (absorbe el daño recibido).
   - Otorga de forma **garantizada** un objeto aleatorio de la lista de loot de la escena.
