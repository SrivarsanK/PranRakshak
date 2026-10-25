# Verification record

Revision A, 25 October 2026. Bench schematic only.

- Tool: KiCad 10.0.7, native `kicad-cli`.
- Four schematic sheets loaded successfully and exported as a four-page PDF.
- Final all-severity ERC reports **0 errors, 68 footprint-review warnings, 0 exclusions**. All four checks disabled by KiCad defaults were also enabled, leaving no checks ignored. Each warning is an intentionally unassigned footprint that cannot match its library filter. These are retained for honest PCB-preparation review, not excluded or suppressed. The violation-sensitive command therefore returns nonzero. The unmodified machine-readable result is `ERC_Report.json`.
- Netlist was exported by KiCad after the final schematic changes. The checks below examine that exported netlist, not merely the drawing generator's intended connections.
- 125 independent connectivity/structural assertions passed, including all 19 ESP module pins, charging/run separation, converter/inductor connections, sensor dividers, heater selector contacts, UART crossing, I2C address/mode pins, flyback diode polarity and intentional no-connects.
- Rendered all four final PDF pages and visually inspected sheet bounds, labels, notes and title blocks.
- Exported schematic component count: 81. Global and local connections total 53 netlist nets including intentional no-connect nets.
- Source PDF SHA-256: `4b5448da5c5a61dc3077283433aa02a93aeb5ae52d017d186b8bf58525b33745`.

## Remaining validation

ERC does not establish analog accuracy, heater timing, runtime, PCB power integrity, external sensor/module compatibility, enclosure performance, firmware behavior, charging fault coverage or intrinsic safety. No hardware prototype, simulation, PCB DRC, sensor calibration or explosive-atmosphere test has been performed.

The complete schematic is editable. Several connectors and raw/proposed parts have no assigned footprint; this is intentional pending exact hardware selection. This package is not an orderable PCB design. References without assigned footprints: C1, C10, C11, C12, C13, C14, C15, C16, C17, C18, C19, C2, C20, C21, C22, C23, C3, C4, C5, C6, C7, C8, C9, D1, D2, F1, F2, J1, J2, J3, J4, J5, J6, J7, J8, L1, R1, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R2, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R3, R4, R5, R6, R7, R8, R9, RV1, S1, S2, SW1, SW2, SW3, SW4, U4, U5.

See Design_Notes.md for the H2S AFE blocker, TP4056 TEMP-short limitation, MQ heater/5 V tolerance checks, incompatible CO timing target and battery-life estimate.
