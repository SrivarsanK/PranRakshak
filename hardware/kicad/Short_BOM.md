# Short BOM - one node

See `BOM.csv` for all 81 schematic references, values, available footprints, assumptions and notes. External devices are listed here even when their schematic reference is an interface connector. Prices and availability have not been quoted.

| Qty | Reference | Part / requirement | Status |
| --- | --- | --- | --- |
| 1 | U1 | Espressif ESP32-C3-WROOM-02-N4 | Named in submission |
| 1 each | S1, S2 | Winsen MQ-4 and proposed MQ-7B raw sensors | MQ-4/MQ-7 named; exact purchased variants unconfirmed |
| 1 | J4 external | H2S electrochemical sensor plus matched, buffered analog front end; 3.3 V, <=20 mA, 0..3.3 V output contract | Exact cell/AFE missing; do not attach a raw cell |
| 1 | U2 | TOPPOWER TP4056-42-ESOP8 | Charger family named; lot-specific current law must be checked |
| 1 | J2 external | Protected 1S 2500 mAh LiPo, >=3 A discharge capability, cell-mounted 10k B3435 NTC | Capacity specified; pack model/protection/NTC proposed |
| 1 each | U3, L1, RV1 | TPS61023DRLR; XEL4030-102ME 1 uH; 100k multiturn trimmer | Proposed 5 V boost; trim and qualify sensor rail |
| 1 each | U4, U5 | LDL1117S33R 3.3 V / TLV1117-15IDCYR 1.5 V LDO | Proposed; thermal and capacitor stability checks required |
| 1 | K1 | Omron G5V-1 DC3 SPDT relay | Proposed bench-only MQ-7 heater selector |
| 1 | J5 external | Sensirion SPS30 with correct 5-pin cable | Proposed dust sensor; airflow/size/coal-dust performance unvalidated |
| 1 | U6 | LIS3DHTR | Proposed man-down motion sensor |
| 1 | J6 external | 1.3-inch SH1106 I2C OLED, true 3.3 V operation | Display named; exact module missing |
| 1 | J8 external | ERM motor rated for 3.3 V, <=100 mA stall current | Vibration specified; exact motor missing |
| 2 each | Q1/Q2, D1/D2 | AO3400A / SS14 | Proposed relay/motor drivers and flyback protection |
| 1 each | SW3, F1, F2 | >=3 A DC break-before-make SPDT; 3 A fast fuse; 0.5 A charge-input fuse | Proposed; confirm mechanical pinout and fault ratings |
| 3 | SW1, SW2, SW4 | Reset, boot, panic momentary switches | Proposed implementation |
| As shown | R1-R29, C1-C23, J1-J8 | Specified passive values and keyed/local connectors; R14/15, R17/18, R23/24, R6/7 use 0.1% ratios | Connector order is a design contract, not universal module pin compatibility |

Use >=10 V capacitors on battery/3.3 V rails and 16 V parts for the boost's 22 uF output ceramics. Check effective capacitance after DC bias. Confirm the actual footprint and voltage, power, temperature and current ratings before ordering. RF module, relay and sensor mechanical outlines need board-level clearance review.
