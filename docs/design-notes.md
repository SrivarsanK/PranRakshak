# Design notes and evidence inventory

[Project README](../README.md) · [Stage 2 submission](stage-2-submission.pdf) · [CAD guide](../cad/README.md) · [KiCad package](../hardware/README.md)

These notes explain how the project description was assembled from the submissions, CAD assets, four-sheet schematic, and separate PCB carrier draft.

## Updated submission · 25 October 2026

The current README uses the [updated 29-page submission](stage-2-submission-updated.pdf), supplied as `Vishwakarma Awards 2026-27 Stage 2 Submission Template.pptx-1.pdf`. The earlier 26-page PDF remains at its original path so historical references and banner provenance stay intact.

| Updated pages | Use in the README |
| --- | --- |
| 1–5 | Identity, mining problem, intended beneficiaries, and proposed worker journey. |
| 6–7, 9 | Proposed architecture, targets, and hardware selection. |
| 11–12 | Electronics narrative and an illustrative ₹13,630 BOM. Visual review confirms page 12 retains a “Project Terraweed Example” label; cost and procurement claims are excluded as verified achievements. |
| 13–18 | Repository links and CAD, schematic, PCB, and FEA evidence slides. Page 14's local computer URL is not a portable report link; the README links the repository's FEA report and PDF. |
| 19 | Maker-journey narrative on a “Project Terraweed Example” slide. The sign-off and performance statements are excluded as verified achievements. |
| 20–26 | Planned safeguards, FMEA, fabrication schedule, technical risks, and proposed mitigations. |
| 27–29 | References and image sources retained in the supplied PDF. |

Pages 8, 10, 12, and 19 are still labeled as examples. Their rover content, latency, runtime, drop-test, cost, procurement, sign-off, and enclosure-performance claims are excluded as demonstrated PRAN RAKSHAK achievements. The native ERC, failing DRC, and assumption-based FEA records remain the basis for the README's engineering status. Page 6 also retains a small rover-style specification box; only the project-specific target paragraph is used.

The original SVG visual system is documented in [assets/readme](../assets/readme/README.md). It adapts the reference README's structure using original artwork and project-specific text. The [FEA PDF](preliminary-lid-fea.pdf) is an unchanged copy of the previously generated and visually verified five-page report.

## Earlier 26-page submission · source map

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
| [Standalone PCB draft](../hardware/pcb/PRAN_RAKSHAK_RevA.kicad_pcb) | Partially routed 52 × 88 mm carrier board with its own ADC, GPIO map, and external-power assumptions. |
| [PCB source package](../hardware/pcb/README.md) | Original board, preview, BOM, pad mapping, routing summary, generator, and source README. |
| [Native PCB DRC review](../hardware/pcb/review/README.md) | 61 rule violations (5 errors, 56 warnings) and 33 unconnected items; report and review conditions included. |
| [Preliminary lid FEA](../simulation/lid-pressure/README.md) | Actual linear-elastic solves under assumed material, loading and supports; tagged meshes, raw outputs, statistics and convergence plots. |

The complete KiCad package from “Create ESP32-C3 KiCad schematic” is preserved under `hardware/kicad/`, with a matching downloadable ZIP. ERC was rerun on the repository copy with KiCad 10.0.7 and reproduced zero electrical errors, 68 `footprint_filter` warnings, no exclusions, and no ignored checks. PDF and netlist export also succeeded from that copy.

The separate PCB package comes from [Explain KiCad EDA Layout](https://chatgpt.com/share/6ade29ec-7dcc-83ee-a8ff-30b51f544990). Its seven original files and ZIP are preserved. KiCad 10.0.7 loaded the board and ran DRC after filling zones in memory, without saving changes to the board. The result is 61 rule violations and 33 unconnected items. Five default checks remain ignored; no matching native schematic was supplied, so schematic parity was not tested.

The earlier schematic's ERC result does not validate this PCB. A synchronized schematic/board pair, passing PCB DRC, original parametric CAD history, fabrication photos, firmware, gateway source, sensor calibration data, and measured hardware performance remain pending.

The user confirmed that the mechanical material is undecided. A preliminary lid study therefore uses an explicitly assumed isotropic polymer, 10 N distributed force, and rigid screw-hole-wall supports. Four actual finite-element solves met the selected successive-mesh criterion for centre deflection and a fixed central stress measure. The study is numerical evidence under assumptions, not physical validation or a material-strength result.

## Specification details still to resolve

- The current CAD assembly represents a generic ESP32 board, one gas-sensor assembly, and a temperature/humidity sensor. The electrical design now includes CH4/CO paths, a conditioned H2S interface, and proposed motion/panic circuitry. Component selection and physical packaging still need to be reconciled with the CAD model.
- The main node target is an eight-hour shift. An example slide's claim of more than sixteen hours is excluded. Revision A's electrical calculations estimate approximately 2.4–3.1 hours under the documented assumptions. Measured battery endurance is pending.
- The proposed MQ-7B heater cycle is 150 seconds, which conflicts with guaranteeing a fresh CO measurement within the submission's ten-second alert target across all phases. A 1 Hz ADC sampling rate does not resolve this sensing limitation.
- Geometry inspection measured the supplied enclosure at 100 × 70 × 25 mm and its lid at 100 × 70 × 3 mm. These differ from the 52 × 88 × 28 mm target. The approximately 120 g mass and IP67 rating remain targets; no selected material, mass validation, ingress test or certification report is supplied.
- Worker location is specified as a nearest-node zone. Exact underground coordinates, leak-source accuracy, and rescue completion within five minutes have not been demonstrated.
- MQTT telemetry and local alarms are the baseline proposal. The submission also discusses BLE, Kinetic Mesh, sub-GHz fallback, and predictive models. No corresponding network implementation or comparative test data is included.
- Revision A proposes SPS30 for dust sensing and LIS3DH for motion; these are engineering selections, with measurement suitability and man-down behavior still to validate. Runoff sensors remain unspecified. The CAD temperature/humidity sensor does not substitute for either environmental subsystem.
- The submission's electronics illustrations remain conceptual source material. The new native KiCad project adds charging, regulation, heater selection, ADC conditioning, and a GPIO map. ERC has been reproduced, but hardware behavior and exact external parts still require electrical review and bench tests. J4 requires a conditioned H2S module; it is not a completed bare-cell analog front end.
- The four-sheet schematic notes identify remaining charging-fault and heater-supply concerns, including the TP4056 temperature-input short limitation. Footprints remain unassigned for 68 reviewed references in that schematic package.
- The standalone PCB is a separate carrier design with an ADS1115, analog dust placeholder, external IMU header, different GPIOs, and no onboard charger/regulator/protection. It has not been cross-checked against the four-sheet schematic, which uses MCU ADC inputs and proposed SPS30/LIS3DH circuitry. Both source packages use the label Revision A; this does not establish electrical equivalence.
- The PCB still has incomplete routing and native DRC findings, including thermal-relief errors and footprint-library review warnings. Its programmatic preview and routing-status text are source records, not a passed KiCad DRC or fabrication record.
- The earlier PDF's page 13 and updated PDF's page 12 show ₹13,630 on example-labeled slides. A confirmed project budget requires reconciled native BOMs and vendor quotes.
- Intrinsic safety and sealing are design requirements. They are not established by the presence of enclosure geometry or a mitigation slide.
- The lid FEA excludes base flexibility, bolted contacts/preload, gasket, helmet, electronics, impact, fatigue and manufacturing anisotropy. Selected displacement/stress-probe convergence does not establish convergence of clamp-region peak stress. Select real material properties, service loads and realistic supports, then validate before making a product decision.

## Planned validation evidence

| Test | Record to publish |
| --- | --- |
| Schematic ERC | Published and reproduced: 0 electrical errors, 68 footprint-review warnings. Footprint resolution remains open. |
| PCB DRC | Published: 61 rule violations (5 errors, 56 warnings), plus 33 unconnected items. Routing, footprint verification, and rule resolution remain open. |
| Schematic/PCB reconciliation | No matching pair supplied. Reconcile ADC, GPIO, sensor, connector, and power choices before checking parity. |
| Lid FEA mesh refinement | Published: four solved meshes, numerical checks and selected-metric convergence under recorded assumptions. Physical material/load/support validation remains open. |
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
