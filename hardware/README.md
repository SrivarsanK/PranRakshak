# KiCad hardware designs

[Project README](../README.md) · [Schematic ZIP](PRAN_RAKSHAK_KiCad.zip) · [Schematic PDF](kicad/Schematic_Review.pdf) · [PCB draft](pcb/README.md)

This folder publishes two separate design packages, both labeled Revision A by their source chats. The four-sheet schematic was produced in “Create ESP32-C3 KiCad schematic”; the standalone PCB carrier was supplied through “Explain KiCad EDA Layout.” They use different circuitry and have not been synchronized.

| Package | Contents | Check status |
| --- | --- | --- |
| [`kicad/`](kicad/README.md) / [schematic ZIP](PRAN_RAKSHAK_KiCad.zip) | Four-sheet native schematic, symbols, BOM, PDF, and verification records. | ERC: 0 electrical errors and 68 footprint-review warnings. |
| [`pcb/`](pcb/README.md) / [PCB ZIP](PRAN_RAKSHAK_KiCad_RevA_Design_Package.zip) | Native carrier board, preview, BOM, pad mappings, routing summary, and generator. | DRC: 61 rule violations (5 errors, 56 warnings), plus 33 unconnected items. |

The 15 schematic-package files, seven PCB-package files, and both original ZIPs are preserved unchanged. Application locks and local preferences are excluded; the PCB `review/` directory contains newly generated integration evidence.

## Open the four-sheet schematic

Use KiCad 10. Open [`kicad/PRAN_RAKSHAK.kicad_pro`](kicad/PRAN_RAKSHAK.kicad_pro), then its schematic. Keep all four schematic sheets, the symbol library, and `sym-lib-table` in the same directory. The project-local library uses `${KIPRJMOD}` so the project can be relocated.

| File | Purpose |
| --- | --- |
| [PRAN_RAKSHAK.kicad_sch](kicad/PRAN_RAKSHAK.kicad_sch) | Main controller, boot/reset, native USB, battery ADC, and sheet hierarchy. |
| [Power.kicad_sch](kicad/Power.kicad_sch) | Battery interface, charging, charge/run selection, boost converter, and regulators. |
| [Gas_Sensors.kicad_sch](kicad/Gas_Sensors.kicad_sch) | MQ gas-sensor interfaces, heater selection, and conditioned H2S module input. |
| [User_And_Environment.kicad_sch](kicad/User_And_Environment.kicad_sch) | Dust, motion, display, panic, and vibration-driver circuitry. |
| [PRAN.kicad_sym](kicad/PRAN.kicad_sym) / [sym-lib-table](kicad/sym-lib-table) | Custom symbols and portable project-local library registration. |
| [BOM.csv](kicad/BOM.csv) / [Short_BOM.md](kicad/Short_BOM.md) | Reference-level BOM and proposed selections; procurement quotes are pending. |
| [Design_Notes.md](kicad/Design_Notes.md) | Requirements, engineering assumptions, calculations, and unresolved parts. |
| [ERC_Report.json](kicad/ERC_Report.json) / [Verification.md](kicad/Verification.md) | Original electrical-rule report and package verification record. |
| [PRAN_RAKSHAK.net](kicad/PRAN_RAKSHAK.net) | KiCad-exported netlist for independent connection inspection. |

## Open the standalone PCB draft

Open [`pcb/PRAN_RAKSHAK_RevA.kicad_pcb`](pcb/PRAN_RAKSHAK_RevA.kicad_pcb) directly in KiCad PCB Editor. The original PCB package includes no `.kicad_pro` or matching `.kicad_sch` file. Read its [integration guide](pcb/README.md) and [DRC review](pcb/review/README.md).

The PCB uses an ADS1115 external ADC, different GPIO and sensor interfaces, and externally regulated power. The schematic above includes MCU ADC paths, proposed SPS30/LIS3DH circuitry, and onboard charging/regulation. Updating the board from that schematic requires design reconciliation.

## Schematic verification

The package was loaded from this repository with KiCad 10.0.7. Four-sheet PDF and netlist exports succeeded. Rerunning all-severity ERC reproduced **0 electrical errors and 68 `footprint_filter` warnings**, with no exclusions or ignored checks. Footprints remain to be selected for those references.

From the repository root, run the following command to produce a new report:

```bash
kicad-cli sch erc --format json --severity-all --exit-code-violations --output ERC-review.json hardware/kicad/PRAN_RAKSHAK.kicad_sch
```

The command returns a nonzero status while warnings remain. The supplied [verification record](kicad/Verification.md) also documents 125 connectivity/structure checks; those are recorded package checks, separate from the ERC rerun performed during repository integration.

## Design status

The four-sheet package is a bench schematic. Its notes estimate 2.4–3.1 hours of runtime under the stated assumptions, below the submission's eight-hour goal. MQ-7B heater cycling limits fresh CO measurement timing, and the exact H2S cell/module and analog front end remain unresolved. Read the [design notes](kicad/Design_Notes.md) before hardware work.

The separate PCB is partially routed and fails native DRC. The review used KiCad 10.0.7 with zones filled in memory, preserving the board file. Five default DRC checks were ignored and schematic parity was not tested. Complete routing, resolve the findings, and create or reconcile a matching schematic before fabrication.

The design is not intrinsically safe or certified for explosive mines. Firmware, calibrated sensing performance, and field validation remain separate deliverables.
