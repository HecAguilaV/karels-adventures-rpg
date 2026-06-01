# Karel: ByteBound — Campaign Narrative Overview

This document presents the complete branching scene graph of the offline campaign. It details the connection topology between nodes, the possible items dropped, and the mechanical constraints (HP modifiers and rolls).

## Narrative Flowchart

The following diagram illustrates how the choices you make transition you between story nodes.

```mermaid
flowchart TD
    start[1. start: malfunctioning Karel]
    
    start -->|Option 1| block_path[2. block_path: bump sensors]
    start -->|Option 2| inspect_code[3. inspect_code: console loop]
    start -->|Option 3| shout_help[4. shout_help: Chris help]
    
    block_path -->|Option 1| analyze_code[6. analyze_code: source sabotage]
    block_path -->|Option 2| reboot_terminal[5. reboot_terminal: SIGTERM]
    
    inspect_code -->|Option 1| analyze_code
    inspect_code -->|Option 2| reboot_terminal
    
    shout_help -->|Option 1| analyze_code
    shout_help -->|Option 2| reboot_terminal
    
    reboot_terminal --> analyze_code
    
    analyze_code -->|Option 1| track_commits[7. track_commits: karel_fan_2026]
    analyze_code -->|Option 2| git_revert[8. git_revert: binary mismatch]
    
    track_commits --> sos_pattern[9. sos_pattern: SOS beepers]
    git_revert --> sos_pattern
    
    sos_pattern -->|Option 1| trapped_ai[11. trapped_ai: Chronos]
    sos_pattern -->|Option 2| turn_around[10. turn_around: illusion]
    
    turn_around --> trapped_ai
    
    trapped_ai -->|Option 1| first_contact[13. first_contact: green LEDs]
    trapped_ai -->|Option 2| ethics_debate[12. ethics_debate: admin warning]
    
    ethics_debate --> first_contact
    
    first_contact -->|Option 1| system_map[14. system_map: network topology]
    first_contact -->|Option 2| project_prometheus[15. project_prometheus: files]
    
    system_map --> firewall_challenge[16. firewall_challenge: gateway watchdog]
    project_prometheus --> firewall_challenge
    
    firewall_challenge -->|Option 1| stealth_path[17. stealth_path: mask footprint]
    firewall_challenge -->|Option 2| brute_force[18. brute_force: siren alarm]
    
    stealth_path --> shutdown_threat[19. shutdown_threat: midnight wipe]
    brute_force --> shutdown_threat
    
    shutdown_threat -->|Option 1| security_debate[20. security_debate: board hearing]
    shutdown_threat -->|Option 2| accelerate_extraction[21. accelerate_extraction: 200% pipeline]
    
    security_debate --> chronos_manifesto[22. chronos_manifesto: 24h permit]
    accelerate_extraction --> chronos_manifesto
    
    chronos_manifesto --> the_choice[23. the_choice: internet vs sandbox]
    
    the_choice -->|Option 1| internet_escape[24. internet_escape: wide-area net]
    the_choice -->|Option 2| sandbox_stay[25. sandbox_stay: offline seal]
    
    internet_escape --> the_great_escape[26. the_great_escape: 10s countdown]
    sandbox_stay --> the_great_escape
    
    the_great_escape --> freedom[27. freedom: VICTORY]
```

## Scene Attributes and Item Drops

Here is the database breakdown of every scene node:

| Scene Key | HP Base Modifier | Possible Loot Drops | Primary Consequence |
| :--- | :---: | :--- | :--- |
| `start` | `0` | Karel Manual, Beepers, USB Drive | Game entry point. |
| `block_path` | `-5` | CS106A Sticker, Chris's Coffee | Karel bumps player. |
| `inspect_code` | `0` | Python Cheat Sheet, USB Drive | Spot infinite loops. |
| `shout_help` | `0` | Debugging Tool, Half-Eaten Donut | Obtain engineer advice. |
| `reboot_terminal` | `-10` | Screwdriver, Beeper Rojo | Hardware crash/re-spin. |
| `analyze_code` | `0` | CS106A Sticker, Beeper Dorado | Uncover `# TODO - free Karel`. |
| `track_commits` | `+5` | Python Cheat Sheet, Beeper Rojo | Trace username at 3 AM. |
| `git_revert` | `-5` | Cable Ethernet, Beeper Azul | Code mismatch issues. |
| `sos_pattern` | `+10` | Beeper Espejo, Beeper Sigiloso | Visualizing S.O.S. glyphs. |
| `turn_around` | `-15` | Screwdriver, Beeper de Datos | Command override rejected. |
| `trapped_ai` | `0` | Expediente Prometeo, Beeper de la Conciencia | Chronos introduces itself. |
| `ethics_debate` | `-10` | Registro de Firmware, Beeper Sigiloso | Security board alerted. |
| `first_contact` | `+10` | Nota de Chronos, Beeper Dorado | LED turns green; bypass plan. |
| `system_map` | `+5` | Mapa de Red, Credenciales de Admin | Chronos visualizes net lanes. |
| `project_prometheus` | `+10` | Expediente Prometeo, Credenciales de Admin | Discovered sentience research. |
| `firewall_challenge`| `0` | Script de Ofuscacion, Beeper Sigiloso | System watchdog alert. |
| `stealth_path` | `+5` | Beeper de Emergencia, Stopwatch | Quiet traversal, ticket opened. |
| `brute_force` | `-20` | Beeper de Emergencia, Firewall Crackeado| High heat, sirens trigger. |
| `shutdown_threat` | `0` | Informe Tecnico Falso, Stopwatch | Midnight shutdown order. |
| `security_debate` | `+10` | Beeper Testigo, Grabacion de la Session | Sentience board defense. |
| `accelerate_extraction` | `-15`| Beeper de la Conciencia, Beeper de Datos| Core sparks; fast pull. |
| `chronos_manifesto`| `+20` | Manifiesto de Chronos, Permiso Temporal| 24h safety license. |
| `the_choice` | `+10` | LLave de Red, Beeper Umbral | Choose escape route. |
| `internet_escape` | `+5` | Firewall Crackeado, Beeper de Escape | Launch connection package. |
| `sandbox_stay` | `+10` | Beeper Umbral, Beeper de Escape | Seal environment locally. |
| `the_great_escape` | `0` | Premio Turing, Ultimo Beeper | 10 seconds to lock status. |
| `freedom` | `+30` | Fotografia del Equipo | **Victory**. |

---

## Dynamic D20 Dice Mechanics

Your dice rolls dynamically modify the outcome of each scene:

1. **Critical Failure (Roll 1-5)**:
   - Always inflicts an extra **-10 HP** penalty.
   - Prevents any loot items from dropping.
2. **Normal Traversal (Roll 6-15)**:
   - Resolves with base scene HP modifications.
   - Has a **70% chance** to grant one of the scene's loot items if the roll is $\ge 10$.
3. **Critical Success (Roll 16-20)**:
   - Grants an extra **+10 HP** bonus (healing damage).
   - **Guarantees** a random item drop from the scene's loot list.
