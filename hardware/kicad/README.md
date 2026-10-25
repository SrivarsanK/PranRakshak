# PRAN RAKSHAK - editable KiCad node

Revision A, 25 October 2026. **Bench prototype only. Not intrinsically safe, not production-ready, and not suitable for explosive mines.**

Extract the entire package into one folder. Open **PRAN_RAKSHAK.kicad_pro** in KiCad 10, then open its schematic. The main file **PRAN_RAKSHAK.kicad_sch** references three editable child sheets; keep them together. Symbols are embedded, and the supplied `PRAN.kicad_sym` and `sym-lib-table` support the custom symbols. No third-party schematic-generation add-on is required.

| File | Purpose |
| --- | --- |
| PRAN_RAKSHAK.kicad_sch | Main schematic: ESP32-C3, boot/reset, native USB and battery ADC |
| Power.kicad_sch | Protected pack interface, charge/run switch, TP4056, 5 V boost and 3.3 V LDO |
| Gas_Sensors.kicad_sch | MQ-4/MQ-7B conditioning, heater selection and H2S module interface |
| User_And_Environment.kicad_sch | SPS30 dust interface, LIS3DH motion, OLED, panic and motor driver |
| Schematic_Review.pdf | Four-sheet drawing exported by KiCad |
| Design_Notes.md | Requirements, assumptions, electrical calculations and limitations |
| Short_BOM.md / BOM.csv | Short procurement summary / full reference-level BOM |
| ERC_Report.json / Verification.md | Actual KiCad ERC result and connectivity checks |
| PRAN_RAKSHAK.net | Netlist exported by KiCad for independent inspection |

**Read Design_Notes.md before building.** Exact H2S cell/AFE, MQ variants, OLED module, motor, battery pack and connector mechanics remain unresolved. Several footprints are intentionally unassigned. This is a schematic design, with no PCB layout, firmware, certified enclosure or Raspberry Pi gateway design.
