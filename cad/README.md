# Sensor-node CAD assembly

[Back to the project](../README.md) · [STEP model](VKA2026.step) · [Original screenshots](../assets/cad/)

`VKA2026.step` is the supplied assembly exchange file for the PRAN RAKSHAK sensor pod. It shows how the enclosure, controller, sensors, power module, and wiring are arranged. The lid is positioned above the enclosure to expose the internal layout.

![Sensor pod assembly and wiring](../assets/cad/assembly-wiring.jpeg)

## File details

| Property | Value |
| --- | --- |
| File | `VKA2026.step` |
| Size | 1,406,956 bytes |
| Format | ISO 10303-21 STEP; `AUTOMOTIVE_DESIGN` / AP214 schema |
| Declared length unit | Millimetres |
| Inspected enclosure envelope | 100 × 70 × 25 mm |
| Inspected lid envelope | 100 × 70 × 3 mm, with four 3.5 mm diameter holes |
| Root product name | `MineSense_Presentation_Assembly` |
| Product definitions | 75, including the root assembly; this is not a fabrication part count |
| Assembly occurrence records | 74 |
| Export tool recorded in header | Open CASCADE STEP processor 7.9 |
| Export timestamp recorded in header | `2026-10-25T13:48:32` (no timezone recorded) |

The root product's original name is preserved inside the file. PRAN RAKSHAK is the project name used in the submission.

## Components represented

| Component group | What the model shows |
| --- | --- |
| Enclosure and lid | Main housing and a separate lid in an exploded position, with mounting features. |
| Controller assembly | ESP32 controller representation, module, USB connector, and header pins. |
| Power management | Power board, regulator, terminals, external power input, and mounting standoffs. |
| Gas sensor | Sensor board representation, cylindrical sensing can, cap, and supporting standoffs. |
| Temperature/humidity sensor | Sensor assembly, package, cover, and mounting standoffs. |
| Wiring | Named power, ground, gas-signal, and temperature-sensor connections. |
| Connection labels | Named terminals and a wire-colour key plate. |

Component names and shapes describe placement. They do not establish exact sensor models, MCU variants, pin assignments, or a manufacturing-ready electrical design.

## Wiring colours in the assembly

| Colour | Labeled use |
| --- | --- |
| Red | Positive supply, controller VIN, temperature-sensor VCC, and external supply positive. |
| Black | Ground connections. |
| Yellow | Gas-sensor signal to the controller ADC. |
| Blue | Gas-sensor VCC / power rail. |
| Orange | Temperature-sensor data to controller GPIO. |

Use these labels to follow the visual assembly. The [Revision A KiCad project](../hardware/README.md) now documents the electrical interfaces separately; its pin map, component selections, and packaging still need to be reconciled with this presentation model before fabrication.

## Open the model

1. Download [VKA2026.step](VKA2026.step), or clone the repository.
2. Import it into a STEP-compatible CAD application.
3. Confirm the import uses millimetres and inspect the assembly/component tree.
4. Examine the enclosure, standoffs, board placement, sensor access, and wiring. The elevated lid is intentional in this presentation.

A STEP import generally provides exchange geometry and assembly structure. Editable sketches, constraints, and the originating design application's parametric history are not supplied with this export.

## Screenshot provenance

All three CAD screenshots are included without image edits. Their repository filenames are shortened for stable README links.

| Repository file | Supplied filename |
| --- | --- |
| [`assembly-wiring.jpeg`](../assets/cad/assembly-wiring.jpeg) | `WhatsApp Image 2026-10-25 at 7.28.04 PM.jpeg` |
| [`assembly-overview.jpeg`](../assets/cad/assembly-overview.jpeg) | `WhatsApp Image 2026-10-25 at 7.27.43 PM.jpeg` |
| [`enclosure-components.jpeg`](../assets/cad/enclosure-components.jpeg) | `WhatsApp Image 2026-10-25 at 7.27.24 PM.jpeg` |

The STEP file is copied without modification, including its embedded export timestamp. Screenshot filenames and Git commit dates describe different events; establishing when the model was first created requires the original design history.

## Scope of this evidence

The published assets document a sensor-pod layout. They do not demonstrate the full multi-gas installation, completed helmet integration, operating firmware, battery endurance, ingress protection, or intrinsic-safety certification. Geometry inspection for the [preliminary lid FEA](../simulation/lid-pressure/README.md) measured the actual envelopes above; the enclosure differs from the submission's 52 × 88 × 28 mm target.
