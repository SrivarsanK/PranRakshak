# PRAN RAKSHAK — Smart Helmet / Sensor Node PCB, Rev A

**Design status: EDITABLE PCB LAYOUT DRAFT. NOT FABRICATION-READY. NOT CERTIFIED FOR MINING.**

This layout was created against the **Vishwakarma Awards 2026–27 Stage 2** project submission supplied by the team. It has **not been electrically cross-checked against a prior native KiCad schematic** (the earlier `.kicad_sch` was not accessible in this chat). Do not call this a completed design, proof of fabrication, passed DRC, or intrinsically safe product.

## Files
- `PRAN_RAKSHAK_RevA.kicad_pcb`: native, editable KiCad PCB file. Standalone board; nets, copper tracks, plated through holes, mounting holes and copper-fill zones are included.
- `PRAN_RAKSHAK_RevA_preview.png`: placement / preliminary copper preview, generated directly from board source objects (not a KiCad DRC screenshot).
- `PRAN_RAKSHAK_RevA_BOM.csv`: footprint/component list (prototype, not vendor-priced final BOM).
- `PRAN_RAKSHAK_RevA_Net_Mapping.csv`: complete pad-to-net mappings for review.
- `PRAN_RAKSHAK_routing_status.txt`: algorithmic routing summary (not a KiCad DRC or ERC result).
- `build_pran_pcb.py`: reproducible source generator.

## Board scope and mechanical target
- Two-layer PCB, nominal **52 × 88 mm** rectangular board; thickness nominal 1.6 mm.
- Four nominal 2.5 mm NPTH mounting holes; enclosure, fastener and clearance fit is still to be checked.
- `U1` ESP32-C3-WROOM-02-N4 Wi-Fi/BLE module, positioned near top edge. Onboard PCB antenna keepout on **all copper layers**, to be verified against latest Espressif module guidelines.
- `U2` ADS1115 VSSOP-10 ADC for 4 external analog sensing channels.
- I2C OLED and IMU header interfaces (both share bus), external panic switch, vibrator and alarm buzzer drivers.
- **No battery charger, no regulated supply, no LiPo battery-protection circuitry is on this PCB**. This is a regulated power *carrier board* to keep the prototype serviceable. It requires separately designed and tested power management. The 3.3 V/5 V inputs are **not** raw LiPo connections.
- Optional external analog sensor and gas breakout boards attach through 2.54 mm headers. This PCB itself is not a calibrated multi-gas instrument.

## Connector pinout — pin 1 first, top to bottom at each header

| Reference | Function | Pins |
|---|---|---|
| J1 | Regulated supply / battery monitor | 1: 3V3; 2: GND; 3: 5V_SENSOR; 4: VBAT_RAW (sense only) |
| J2 | MQ-4 CH4 breakout | 1: 5V_SENSOR; 2: GND; 3: CH4_RAW (0–5 V assumed) |
| J3 | MQ-7 CO breakout | 1: 5V_SENSOR; 2: GND; 3: CO_RAW (0–5 V assumed) |
| J4 | H2S analog signal-conditioning board | 1: 3V3; 2: GND; 3: H2S_AIN (0–3.3 V max) |
| J5 | Analog dust interface (placeholder) | 1: 5V_SENSOR; 2: GND; 3: DUST_RAW (0–5 V assumed) |
| J6 | OLED I2C header | 1: 3V3; 2: GND; 3: SDA; 4: SCL |
| J7 | IMU I2C header | 1: 3V3; 2: GND; 3: SDA; 4: SCL |
| J8 | Panic button | 1: PANIC; 2: GND |
| J9 | Vibration motor | 1: 3V3; 2: MOTOR_LOW (MOSFET drain) |
| J10 | Buzzer / alarm | 1: 3V3; 2: BUZZ_LOW (MOSFET drain) |
| J11 | USB data test pads/header only | 1: GND; 2: USB_DM; 3: USB_DP; not a USB-C connector |
| J12 | Reset external pushbutton | 1: EN; 2: GND |
| J13 | BOOT external pushbutton | 1: BOOT/GPIO9; 2: GND |

**Connector warning:** These labels describe proposed *board pinouts*, not the definitive pinouts of any third-party sensor breakout. Wire by pin labels after checking your exact modules. Do not plug unknown modules in based only on connector shape.

## Electrical rationale and unverified assumptions
1. MQ-4/MQ-7 and the *placeholder analog dust breakout* each use a **12k/20k divider**, bringing 5.0 V maximum analog output to **3.125 V**, below a nominal 3.3 V ADS1115 supply. ADC PGA/full-scale, analog absolute maximum and sensor heater requirements still require verification. Divider output must stay within device input limits under tolerance and power sequencing; consider clamping and low-leakage filtering.
2. H2S input requires a **manufacturer-appropriate electrochemical analog front end and calibration** before connecting to J4; a raw electrochemical cell **must not be connected directly**.
3. `U2` ADS1115 uses I2C with ADDR pin tied to GND (typical address 0x48). `R3`/`R4` are 4.7k I2C pull-ups; verify that OLED and IMU breakouts do not introduce excessive parallel pull-up loading.
4. VBAT_RAW on J1 is **voltage sense only**, via 100k+100k dividers to ESP32 GPIO4 ADC. Protected battery/power converter must ensure the sense line cannot power the microcontroller via input clamps when the 3V3 rail is absent.
5. Status LED on GPIO5; ESP32-C3 GPIO6/7 used for I2C; GPIO9 (strapping) via external BOOT switch/pull-up; GPIO10 panic; GPIO20 vibration; GPIO21 buzzer; USB D-/D+ on GPIO18/19. GPIO2 and GPIO8 remain unassigned to avoid interfering with boot straps.
6. `Q1` and `Q2` proposed AO3400A MOSFET low-side drivers, with flyback diodes. Confirm gate/driver logic, actual SOT-23 land pattern, inductive load current, startup conditions, and external motor/buzzer operating voltage. The alarm loads are currently wired to **3V3**, not direct battery voltage.
7. **3.3 V AND regulated sensor 5 V must be externally generated** with proper over-current, over-temperature, LiPo charging/protection, brownout and EMC design. TP4056 charging and any boost/buck-boost converter from the team's submission are *not yet implemented* on this PCB.
8. Gas diffusion openings, IP67 sealing, temperature effects, heated sensor power and dust filtering are separate mechanical/system tasks. An IP67 enclosure alone does not guarantee a safe gas-sensing chamber.
9. Dust, water-runoff, airflow, and long-range mesh radio node capabilities from the overall proposal are **not implemented** by this single PCB. The Raspberry Pi gateway is a separate computer.

## Remaining work before fabrication
- Obtain the exact sensor MPNs/module datasheets, mechanical housing and verified 3.3 V/5 V power module.
- Get or recreate the matching **KiCad `.kicad_sch`**; synchronize the netlist and footprint assignments via *Tools → Update PCB from Schematic*.
- **Complete unrouted nets**, specifically SDA/SCL, the panic input, parts of 3V3 and analog/driver connections. This layout intentionally contains unrouted airwires after an automated short-risk removal pass. **Never send to fabrication yet.**
- **Fill ground copper zones** in KiCad (`B`) and verify every GND pad belongs to a continuous return path; add ground stitching and decoupling vias as necessary.
- Run KiCad **DRC** after the copper pours fill. No genuine KiCad DRC has been run; there is no guarantee of zero shorts, zero dangling nets, zero footprint/silkscreen/edge violations, or correct creepage/clearance.
- Examine module antenna-to-copper/metal/battery clearance using Espressif guidance and the actual enclosure (RF + EMI tests).
- Confirm ADS1115 VSSOP package pin-1 orientation and pad dimensions against the datasheet and actual MPN. Verify the custom MCU footprint using an official current KiCad/Espressif library before release.
- Build a current budget using **measured MQ-4/MQ-7 heater currents**, Wi-Fi bursts, alarm peaks, and charging losses. The claimed eight-hour wearable runtime is an engineering **target**, not proven by this file.
- Use a gas-safety professional and the applicable jurisdiction's intrinsic-safety / explosion-protection process before field deployment. An ordinary ESP32+LiPo+MQ heater PCB is not certified for explosive mine atmospheres. Bench testing only, in a safe environment.

## Verification completed here
- Native KiCad PCB board source written with 49 references, 27 named electrical nets, copper tracks and copper-layer keepouts.
- Component pin mappings exported to CSV; board has 52 × 88 mm perimeter.
- Preliminary programmatic *short-overlap check* of explicitly routed copper objects passed at a **0.16 mm combined geometry expansion screen**. This is **not** a manufacturability clearance check, not a full net-continuity test, and does not replace KiCad DRC.

## References
- Espressif ESP32-C3-WROOM-02 Datasheet: https://documentation.espressif.com/esp32-c3-wroom-02_datasheet_en.html
- Espressif ESP32-C3 design guide: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/schematic-checklist.html
- Texas Instruments ADS1115 datasheet: https://www.ti.com/lit/ds/symlink/ads1115.pdf
