# Design notes and evidence inventory

[Project README](../README.md) · [Stage 2 submission](stage-2-submission.pdf) · [CAD guide](../cad/README.md) · [KiCad package](../hardware/README.md)

These notes explain how the project description was assembled from the supplied submission, CAD assets, and Revision A electrical design. Page numbers refer to the 26-page submission PDF.

## Source map

| Pages | Content used |
| --- | --- |
| 1–3 | Project identity, team ID, mining theme, problem statement, and proposed smart-helmet concept. |
| 4–5 | Target users and the proposed before/after workflow. Rescue-time and early-warning statements are aspirations. |
| 7–8 | System architecture, hardware selection, and target specifications. Diagram-only labels were reviewed visually as well as extracted text. |
| 10, 12 | Node/gateway roles and conceptual electronics architecture. The drawing on page 12 is reference design material, not an editable schematic or an electrical-check report. |
| 17–18 | Proposed fault handling and hazard mitigation. |
| 19–20 | Design FMEA and October 2026–January 2027 fabrication plan. |
| 21–23 | Calibration, placement, ventilation, communication, synchronization, and power risks; suggested mitigations. |
| 24–26 | External references and image-source credits retained in the original PDF. |

Pages 6, 9, 11, 13, and 16 are explicitly marked as examples, with unrelated agricultural-rover content and illustrative specifications. The README excludes their cost, procurement, fabrication, faculty-signoff, drop-test, and enclosure-performance statements as evidence of PRAN RAKSHAK achievements.

Pages 14–15 contain maker-evidence guidance rather than fabrication results.

Page 7's small illustrated specification box includes rover-style payload, speed, and power figures inconsistent with the mine-safety narrative. The README uses the adjacent project-specific target paragraph instead. A leftover tiller-related label on page 19 is excluded from the mining FMEA description.

## Published evidence

| Asset | What can be reviewed |
| --- | --- |
| [`VKA2026.step`](../cad/VKA2026.step) | Supplied assembly exchange geometry and named components. |
| [Three CAD screenshots](../assets/cad/) | CAD workspace, component browser, enclosure layout, wiring, and exploded lid. |
| [Submission PDF](stage-2-submission.pdf) | Proposed system, targets, planned mitigations, and fabrication schedule. |
| [Native KiCad project](../hardware/kicad/PRAN_RAKSHAK.kicad_pro) | Four editable schematic sheets and a project-local symbol library. |
| [Schematic PDF](../hardware/kicad/Schematic_Review.pdf) | Four-sheet drawing exported by KiCad. |
| [BOM](../hardware/kicad/BOM.csv) | Reference-level components; proposed parts and open selections are explained in the short BOM. |
| [ERC and verification record](../hardware/kicad/Verification.md) | Zero electrical errors and 68 footprint warnings; the supplied record also documents 125 connection/structure checks. |

The complete KiCad package from “Create ESP32-C3 KiCad schematic” is preserved under `hardware/kicad/`, with a matching downloadable ZIP. ERC was rerun on the repository copy with KiCad 10.0.7 and reproduced zero electrical errors, 68 `footprint_filter` warnings, no exclusions, and no ignored checks. PDF and netlist export also succeeded from that copy.

PCB layout/DRC, original parametric CAD history, fabrication photos, FEA results, firmware, gateway source, sensor calibration data, and measured hardware performance results remain pending. ERC is a schematic check; it does not establish those outcomes.

## Specification details still to resolve

- The current CAD assembly represents a generic ESP32 board, one gas-sensor assembly, and a temperature/humidity sensor. The electrical design now includes CH4/CO paths, a conditioned H2S interface, and proposed motion/panic circuitry. Component selection and physical packaging still need to be reconciled with the CAD model.
- The main node target is an eight-hour shift. An example slide's claim of more than sixteen hours is excluded. Revision A's electrical calculations estimate approximately 2.4–3.1 hours under the documented assumptions. Measured battery endurance is pending.
- The proposed MQ-7B heater cycle is 150 seconds, which conflicts with guaranteeing a fresh CO measurement within the submission's ten-second alert target across all phases. A 1 Hz ADC sampling rate does not resolve this sensing limitation.
- The 52 × 88 × 28 mm envelope, approximately 120 g mass, and IP67 enclosure are targets. No dimension comparison, mass calculation, ingress test, or certification report has been supplied.
- Worker location is specified as a nearest-node zone. Exact underground coordinates, leak-source accuracy, and rescue completion within five minutes have not been demonstrated.
- MQTT telemetry and local alarms are the baseline proposal. The submission also discusses BLE, Kinetic Mesh, sub-GHz fallback, and predictive models. No corresponding network implementation or comparative test data is included.
- Revision A proposes SPS30 for dust sensing and LIS3DH for motion; these are engineering selections, with measurement suitability and man-down behavior still to validate. Runoff sensors remain unspecified. The CAD temperature/humidity sensor does not substitute for either environmental subsystem.
- The submission's electronics illustrations remain conceptual source material. The new native KiCad project adds charging, regulation, heater selection, ADC conditioning, and a GPIO map. ERC has been reproduced, but hardware behavior and exact external parts still require electrical review and bench tests. J4 requires a conditioned H2S module; it is not a completed bare-cell analog front end.
- The KiCad notes identify remaining charging-fault and heater-supply concerns, including the TP4056 temperature-input short limitation. The design is a bench prototype schematic and has no PCB layout or assigned footprints for 68 reviewed references.
- Page 13's ₹13,630 total belongs to an example BOM. A confirmed project budget should be published after a project-specific BOM and quotes are available.
- Intrinsic safety and sealing are design requirements. They are not established by the presence of enclosure geometry or a mitigation slide.

## Planned validation evidence

| Test | Record to publish |
| --- | --- |
| Schematic ERC | Published and reproduced: 0 electrical errors, 68 footprint-review warnings. Footprint resolution remains open. |
| Gas calibration and drift | Reference concentrations, sensor identification, conditions, error, and repeat readings. |
| Alert latency | Timestamped threshold crossing and observed local warning, compared with the under-10-second target. |
| Node loss | Last received heartbeat and time the gateway marks the node missing. |
| Man-down behavior | Motion/inactivity trials, trigger timing, and false-alarm observations. |
| Offline operation | Local telemetry, alarms, and logging with the external internet connection removed. |
| Zone localization | Mapped node positions and observed versus reported worker zones. |
| Power and endurance | Measured current profile, heater cycle, battery conditions, and runtime. |
| Fault handling | Stale packets, sensor disconnection, gateway loss, watchdog, and brownout results. |

## Documentation reference

The section flow and use of captioned visuals are inspired by [dmunish/reach](https://github.com/dmunish/reach#readme). PRAN RAKSHAK's technical claims are based on the supplied project materials.
