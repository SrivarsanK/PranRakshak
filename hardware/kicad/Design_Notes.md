# PRAN RAKSHAK - design notes

Revision A, 25 October 2026. **Non-hazardous bench prototype only. This circuit is NOT intrinsically safe or production-ready for explosive mines.** Fuses, current limiting, flame-resistant material, an enclosure mesh, a radio module approval or a clean ERC do not establish intrinsic safety. Formal intrinsic safety certification and the applicable mining approvals require a qualified hazardous-area engineering and certification process. Hot MQ heaters, relay arcing, battery energy, converter inductance, stored capacitor energy and exposed connectors are unresolved ignition sources.

## Submission requirements versus engineering choices

The source is the attached 26-page `Vishwakarma Awards 2026-27 Stage 2 Submission Template.pptx(1).pdf`, recovered from the referenced chat. Its example slides contain reused TerraWeed labels and conflicting performance claims; these are treated as design proposals, not measured results.

| Source | Specified or depicted | Treatment in this schematic |
| --- | --- | --- |
| pp7-10,13 | ESP32-C3-WROOM-02-N4; MQ-4 CH4, MQ-7 CO, electrochemical H2S; Wi-Fi/MQTT to Raspberry Pi | MCU and gas interfaces included; Wi-Fi is internal to module. MQ-7B is an explicitly proposed variant. |
| p8 visual diagram | Dust sensing, motion/man-down, panic button, OLED | Proposed SPS30, LIS3DH and button circuitry; OLED interface included. |
| pp7,9 | Helmet vibration and OLED warning; 1 Hz sampling; <10 s alerts; 30 s no-motion/lost-node flags | Motor driver and sensing hardware included. Timing, detection and networking need firmware and performance validation. |
| pp7,9,11-13 | 3.7 V 2500 mAh LiPo, TP4056, 3.3 V LDO | Protected pack/NTC, charge/run interlock, discrete boost and LDO implementation proposed. TP4056 is a charger, not discharge protection. |
| p7/p9 versus p11 | 8 h battery versus >16 h battery; heater duty cycling | Neither endurance claim accepted. See power estimate below. |
| pp8,12-13 | Pi 4, logging, gateway OLED/siren; fixed-node runoff/water sensing | Gateway is outside this node design. A local 3.3 V expansion connector is provided; undefined water sensors require separate interfaces. |

Exact sensor procurement models are missing. In particular, **J4 is a conditioned H2S module interface, not a completed electrochemical cell AFE**. It requires a 3.3 V, <=20 mA module with buffered, nonnegative, ground-referenced 0..3.3 V output. Cell bias, transimpedance gain, zero current, sensitivity, polarity, cross-sensitivity and range cannot be chosen responsibly without its datasheet. Do not connect a bare cell to J4. OLED, battery/NTC, motor, sensor cables and package footprints must also be finalized.

## Power and charging

J2 accepts a protected single-cell pack: pin 1 positive, pin 2 ground, pin 3 cell-mounted NTC. Select documented overcharge, undervoltage and short-circuit protection with >=3 A discharge capability. F1 is a proposed 3 A ordinary fuse, not an intrinsic-safety energy barrier. Input polarity is not electronically protected; use keyed wiring and check it before connection.

SW3 is a break-before-make, >=3 A DC switch: common pin 1 to fused pack, throw 2 to charger BAT, throw 3 to BAT_RUN. CHARGE disconnects every node load; RUN disconnects the charger BAT terminal. This avoids the TP4056 termination error caused by simultaneous system loading. It is not a power-path/load-sharing charger. J3 needs a regulated, current-limited 5 V source; F2 is 0.5 A. Charge only in a non-hazardous area.

R8=6.04k gives about 182 mA using the retrieved TOPPOWER 1100/RPROG law, or 199 mA with the common 1200/RPROG variant. Confirm the purchased IC revision and measure charge current, 4.2 V regulation and termination. At 200 mA and 5.25 V input/3.0 V cell, dissipation is about 0.45 W; provide exposed-pad copper and verify temperature. A 2500 mAh pack will need well over 12 hours including the CV phase, depending on the actual charge current.

R9=6.8k above a 10k B3435 NTC gives a nominal charge window around 1..41 C for 0.80/0.45 supply-ratio thresholds. IC thresholds, NTC curve and tolerances must be qualified against the actual cell's allowed range. Open-circuit NTC should inhibit charging. **A short to ground can disable TP4056 temperature sensing**; this design does not provide independent NTC-short detection. That is a release blocker for unattended charging.

U3 boosts BAT_RUN to V5. Its 0.595 V typical reference gives V5=VFB*(1+Rtop/100k). R10+RV1 allow adjustment; set 5.000 V using a dummy load before attaching sensors. Reference tolerance means a nominal resistor ratio alone cannot guarantee the MQ requirement of 4.90..5.10 V. Measure that range at the sensor pins over battery, temperature and load; redesign the rail if it fails. L1 needs adequate saturation/ripple current, and C7 must retain >=10 uF after DC bias. Keep the switching loop short.

U4 is a ceramic-capacitor-compatible 1.2 A LDL1117S33R fed from regulated V5, rather than directly from a LiPo that may fall below LDO headroom. Reserve >=0.5 A for ESP transients plus motor/relay/peripherals. Regulator loss is (5-3.3)*I: 0.425 W at 250 mA, 0.85 W at 500 mA. The tab is VOUT, not ground. Size copper and validate stability, startup and temperature; no PCB thermal result is claimed. Do not substitute an older 1117 blindly. U5 supplies 1.5 V; its 47 uF capacitor has a 0.22-ohm series return for ESR control, requiring confirmation against the procured TLV1117 revision.

Use a preliminary 5 V peak budget of 1.2 A. At 3.2 V and 85% boost efficiency that represents about 2.21 A from the pack. Verify converter minimum current limit, inductor saturation, fuse heating, wiring and pack capability at cold/low battery. The boost's switching-current limit is not a precision output-current limit.

## Sensor conditioning and performance limits

S1/S2 are **raw six-pin** sensors with pins 1/3 electrode A, 4/6 electrode B, and 2/5 heater under the proposed Winsen pinout. Common MQ breakout boards tie heater and sensing supplies differently and are not interchangeable with these connections. Confirm the actual model and bottom-view numbering.

MQ-4 needs 5.0 V +/-0.1 V and up to 1 W heater power, with initial preheat of at least 48 hours in the retrieved manufacturer manual. It remains heated continuously here. MQ-7B needs 60 s at 5 V followed by 90 s at 1.5 V; K1 selects those rails. GPIO7 high selects 5 V, low selects 1.5 V. Coil drive defaults off/low heat. Sample calibrated CO in the specified low-temperature phase, after startup cleaning and settling. The relay gives rail isolation but is an explicit bench compromise with arcing, wear and power costs.

**A 1 Hz ADC acquisition does not deliver a fresh, calibrated 1 Hz CO measurement.** The 150 s thermal cycle is incompatible with guaranteeing the submission's <10 s CO alert target across all phases. A suitable continuously measuring, certified sensing technology and validated firmware would be needed to meet that requirement. Arbitrary MQ-4 heater duty cycling also invalidates an untested calibration.

Each gas ADC input has a 150k/100k divider and 100 nF shunt capacitor: gain 0.4, Thevenin resistance 60k, time constant 6 ms, pole about 26.5 Hz. A 5.25 V gas signal gives 2.10 V; 0.1% resistor tolerances raise this by only about 0.12%. A 3.3 V H2S module output becomes 1.32 V. These stay below the ESP32-C3 2.5 V measurable range at 12 dB attenuation. The 10k MQ load is additionally loaded by 250k, giving 9.615k effective RL; calibrate the complete circuit. Battery ADC uses the same divider: 4.25 V becomes 1.70 V.

Use ADC1, eFuse calibration, sufficient settling and averaging. The capacitor supplies sampling charge, but ADC acquisition error, leakage, rail coupling and low-end nonlinearity still need measurement; add buffers if required. The dividers are not surge barriers or fault-tolerant clamps. Final cable ESD, overvoltage/reverse-signal protection and sensor supply-fault behavior depend on the selected assemblies. Never hot-plug gas modules or feed negative/raw-cell outputs.

SPS30 is a proposed 5 V dust sensor, not proof of accurate respirable coal-dust measurement. It can draw 65 mA measuring and 80 mA during fan startup. Its UART output is compatible with 3.3 V logic; pin 4 SEL floats for UART. Account for ESP ROM UART0 chatter. Its fan and required airflow challenge the submission's size, weight and IP67 enclosure targets. LIS3DH enables motion sampling; a validated man-down algorithm and worker trials are not supplied.

## GPIO and boot constraints

| ESP GPIO | Physical module pin | Use |
| --- | --- | --- |
| 0 / 1 / 3 / 4 | 18 / 17 / 15 / 3 | ADC1: CH4 / CO / H2S / battery |
| 5 / 6 | 4 / 5 | I2C SDA / SCL, 3.3 V pullups |
| 7 | 6 | MQ-7 high-temperature selector |
| 8 | 7 | Panic, active low, external 10k pullup |
| 9 | 8 | BOOT button, external 10k pullup |
| 2 | 16 | Reserved strap with 10k pullup |
| 10 | 10 | Haptic motor driver |
| 18 / 19 | 13 / 14 | Native USB D- / D+ |
| 20 / 21 | 11 / 12 | Dust UART RX / TX |

GPIO2/8/9 are straps. GPIO9 high permits normal SPI boot; GPIO8 may be either level then. For download, keep GPIO2/8 high and GPIO9 low. Release PANIC during download. EN has 10k/1uF delay and reset button. GPIO5 is ADC2 on this chip; current ESP-IDF documents ADC2 limitations, so it is not used as an ADC here. I2C defaults to 100 kHz with one pair of 4.7k pullups; address LIS3DH=0x18, OLED normally 0x3C/0x3D. Check display pullups and pin order.

J1 is a self-powered micro-USB debug connector. Its VBUS is deliberately unconnected. Use RUN and the battery during flashing; it does not charge the pack. Keep D+/D- routing short and controlled impedance and finalize ESD/EMC protection on the board. Firmware must disable application console output on the dust UART and reject startup chatter as data.

## Battery life and release limitations

A nominal pack contains 3.7*2.5=9.25 Wh. Using 80% usable energy and 85% boost efficiency leaves about 6.29 Wh delivered to the 5 V system. MQ-4 alone is near 1 W; MQ-7 thermal averaging adds roughly 0.38 W using its nominal 30-ohm heater resistance, before MCU, dust fan, display and LDO losses. Heater resistance changes with temperature, so measure actual energy. At an assumed 2.0..2.6 W average 5 V load, endurance is only about **2.4..3.1 hours**, not an accepted 8-hour or 16-hour result. Even at the claimed 1 W system load, this conservative budget gives about 6.3 hours.

Before a powered prototype: finalize models/pinouts/footprints; verify charger with a battery simulator and NTC fault cases; trim rails under dummy loads; check boot with panic pressed/released; capture Wi-Fi/motor/heater transients and temperatures; calibrate certified test gases over environment and sensor ageing; measure actual battery discharge and alarm response. Firmware for brownout handling, watchdogs, stale-data rejection, local alarms, motion timing and MQTT is not included. No enclosure IP, antenna, mesh routing, localization, gateway or explosive-atmosphere qualification is claimed.

## Checks and primary references

KiCad 10.0.7 successfully loaded all four sheets and exported the drawing/netlist. Final ERC includes all severities, enables even the checks disabled by default, and uses no exclusions: **0 errors and 68 warnings for intentionally unassigned footprints**. The schematic passes its electrical connectivity checks; the footprint warnings remain visible for PCB preparation. See `ERC_Report.json` and `Verification.md`. Custom LIS3DH pin types reflect I2C mode (SA0 input and SDA bidirectional); USB supply pins are passive for this self-powered connector. These are electrical-mode definitions, not suppressed ERC findings. ERC cannot verify external module internals, calibration, charging fault coverage or intrinsic safety.

Sources checked 25 October 2026:

- [Espressif ESP32-C3-WROOM-02 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c3-wroom-02_datasheet_en.pdf): physical pins, straps, supply and EN timing.
- [Espressif ADC ranges](https://docs.espressif.com/projects/esp-idf/en/release-v4.4/esp32c3/api-reference/peripherals/adc.html) and [current ADC driver limitations](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-reference/peripherals/adc/adc_oneshot.html).
- [Winsen MQ-4 manual](https://www.winsen-sensor.com/d/files/manual/mq-4.pdf) and [MQ-7B manual](https://www.winsen-sensor.com/d/files/manual/mq-7b.pdf): raw sensor pinning, heater requirements and preheat.
- [TOPPOWER TP4056 datasheet via LCSC](https://www.lcsc.com/datasheet/C16581.pdf): pinout, charge-current law and TEMP behavior; the hosted retrieval was partial, so confirm the actual supplier PDF/revision before procurement.
- [TI TPS61023](https://www.ti.com/lit/ds/symlink/tps61023.pdf), [TI TLV1117](https://www.ti.com/lit/ds/symlink/tlv1117.pdf), and [ST LDL1117](https://www.st.com/resource/en/datasheet/ldl1117.pdf): regulation and capacitor/current constraints.
- [ST LIS3DH](https://www.st.com/resource/en/datasheet/lis3dh.pdf), [Sensirion SPS30](https://sensirion.com/media/documents/8600FF88/64A3B8D6/Sensirion_PM_Sensors_Datasheet_SPS30.pdf), and [Omron G5V-1](https://omronfs.omron.com/en_US/ecb/products/pdf/en-g5v_1.pdf): proposed peripheral interfaces and relay family. Relay terminal assignments also checked against the installed KiCad symbol.
