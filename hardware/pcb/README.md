# Standalone PCB carrier draft

[Project README](../../README.md) · [Hardware designs](../README.md) · [Original PCB ZIP](../PRAN_RAKSHAK_KiCad_RevA_Design_Package.zip)

This is the PCB package supplied through [Explain KiCad EDA Layout](https://chatgpt.com/share/6ade29ec-7dcc-83ee-a8ff-30b51f544990). It contains a partially routed, nominal 52 × 88 mm, two-layer carrier board. The seven source files and original ZIP are preserved unchanged; the `review/` folder adds native KiCad integration evidence.

## Open the board

Open [PRAN_RAKSHAK_RevA.kicad_pcb](PRAN_RAKSHAK_RevA.kicad_pcb) directly in KiCad PCB Editor. The package includes no project configuration or matching schematic. KiCad 10.0.7 successfully loaded it for DRC and layer export.

| Supplied file | Purpose |
| --- | --- |
| [PRAN_RAKSHAK_RevA.kicad_pcb](PRAN_RAKSHAK_RevA.kicad_pcb) | Editable board, footprint placement, preliminary copper, zones, and keepouts. |
| [PRAN_RAKSHAK_RevA_preview.png](PRAN_RAKSHAK_RevA_preview.png) | Source-generated placement/copper illustration; not a KiCad DRC screenshot. |
| [PRAN_RAKSHAK_RevA_BOM.csv](PRAN_RAKSHAK_RevA_BOM.csv) | Board-specific component list. |
| [PRAN_RAKSHAK_RevA_Net_Mapping.csv](PRAN_RAKSHAK_RevA_Net_Mapping.csv) | Board-specific pad-to-net assignments. |
| [PRAN_RAKSHAK_RevA_README.md](PRAN_RAKSHAK_RevA_README.md) | Original design rationale, interfaces, and limitations. |
| [PRAN_RAKSHAK_routing_status.txt](PRAN_RAKSHAK_routing_status.txt) | Original algorithmic routing summary. |
| [build_pran_pcb.py](build_pran_pcb.py) | Supplied generator source, retained without execution during repository integration. |

The original README and routing summary describe the source package's checks. The newer [repository review](review/README.md) records native KiCad DRC performed after import.

## Scope and relationship to the schematic

Both this board and the earlier schematic are labeled Revision A by their source chats. Their circuitry differs:

| Area | This PCB carrier | Earlier four-sheet schematic |
| --- | --- | --- |
| Gas conversion | ADS1115 external ADC. | ESP32-C3 ADC paths. |
| Dust sensing | Analog dust-signal placeholder. | Proposed SPS30 UART interface. |
| Motion | External I2C IMU header. | Proposed LIS3DH circuitry. |
| Power | External regulated 3.3 V and 5 V inputs; no charger, regulator, or battery protection. | Battery interface, TP4056 charging, boost converter, regulators, and heater selection. |
| Pin assignments | Board-specific GPIO and connector map. | Different GPIO and connector assignments. |

The board has not been synchronized with the earlier schematic. Verify the source BOM, pad mapping, footprints, and exact external sensor/power modules before creating or reconciling a matching schematic.

## Native review result

[DRC_Report.json](review/DRC_Report.json) records **61 rule violations (5 errors, 56 warnings), plus 33 unconnected items**. Five default checks remain ignored; schematic parity was not tested. The review filled zones in memory and did not save changes to the supplied board. [PCB_Layers.svg](review/PCB_Layers.svg) is a native KiCad layer export of the stored draft.

This board is not fabrication-ready or certified for explosive mine environments. Finish routing, resolve DRC findings, verify the footprint and antenna design, and validate power and sensor interfaces before fabrication.
