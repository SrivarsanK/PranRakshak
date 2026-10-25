# ESP32-C3 node schematic

[Project README](../README.md) · [Download the KiCad package](PRAN_RAKSHAK_KiCad.zip) · [Schematic PDF](kicad/Schematic_Review.pdf)

Revision A, 25 October 2026. This folder publishes the complete editable schematic package produced in “Create ESP32-C3 KiCad schematic.” The 15 supplied package files and ZIP are copied unchanged. Application locks and local preferences are excluded.

## Open in KiCad

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

## Verification

The package was loaded from this repository with KiCad 10.0.7. Four-sheet PDF and netlist exports succeeded. Rerunning all-severity ERC reproduced **0 electrical errors and 68 `footprint_filter` warnings**, with no exclusions or ignored checks. Footprints remain to be selected for those references.

From the repository root, run the following command to produce a new report:

```bash
kicad-cli sch erc --format json --severity-all --exit-code-violations --output ERC-review.json hardware/kicad/PRAN_RAKSHAK.kicad_sch
```

The command returns a nonzero status while warnings remain. The supplied [verification record](kicad/Verification.md) also documents 125 connectivity/structure checks; those are recorded package checks, separate from the ERC rerun performed during repository integration.

## Design status

This is a bench schematic with no PCB layout or DRC result. The notes estimate 2.4–3.1 hours of runtime under the stated assumptions, below the submission's eight-hour goal. MQ-7B heater cycling limits fresh CO measurement timing, and the exact H2S cell/module and analog front end remain unresolved. Read the [design notes](kicad/Design_Notes.md) before hardware work.

The design is not intrinsically safe or certified for explosive mines. Firmware, calibrated sensing performance, and field validation remain separate deliverables.
