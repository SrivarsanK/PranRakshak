<p align="center">
  <img src="assets/pran-rakshak-banner.svg" alt="PRAN RAKSHAK — offline safety monitoring for underground mines" width="100%">
</p>

<p align="center">
  <strong>Worker health, safety, and environmental hazard tracking.</strong><br>
  Vishwakarma Awards 2026–27 · Stage 2 · Team Codemium
</p>

<p align="center">
  <a href="#the-problem">The problem</a> ·
  <a href="#system-architecture">Architecture</a> ·
  <a href="#cad-and-design-evidence">CAD gallery</a> ·
  <a href="cad/VKA2026.step">STEP model</a> ·
  <a href="docs/stage-2-submission.pdf">Stage 2 submission</a> ·
  <a href="#roadmap">Roadmap</a>
</p>

## PRAN RAKSHAK

PRAN RAKSHAK is a mine safety project designed to detect underground hazards, warn workers locally, and help rescue teams identify a worker's last-known zone. The proposed system combines helmet-mounted sensing, fixed monitoring nodes, and a Raspberry Pi gateway that can operate without a continuous internet connection.

Its scope covers methane, carbon monoxide, and hydrogen sulfide monitoring, with dust exposure and mine-runoff quality monitoring included in the wider environmental design. A panic button and motion-based man-down detection support worker distress alerts.

> **Current stage:** CAD design and prototype planning. This repository contains the supplied STEP assembly, three original CAD screenshots, and the Stage 2 submission PDF. Firmware, gateway software, calibration records, and field-test results have not yet been added. Performance figures below are design targets.

<p align="center">
  <img src="assets/cad/assembly-wiring.jpeg" alt="CAD view of the sensor enclosure with an exploded lid, ESP32 board, gas sensor, power module, and color-coded wiring" width="100%">
  <br><sub>Sensor-node assembly: enclosure, electronics, wiring, and removable lid shown in the CAD workspace.</sub>
</p>

## The problem

Underground miners can encounter toxic gases and respirable dust in areas with intermittent communication and limited visibility. Manual checks leave gaps between readings. If a worker becomes unresponsive, a team also needs to know where to search.

The Stage 2 submission identifies three connected monitoring gaps:

- Gas and dust exposure can build up between handheld inspections.
- Separate monitoring and communication systems delay distress alerts and worker location updates.
- Mine runoff may reach surrounding waterways before manual water-quality checks identify contamination.

PRAN RAKSHAK is intended for miners, ventilation officers, environmental monitoring teams, and rescue squads working across tunnels and nearby catchment areas.

## The proposed solution

Helmet-mounted nodes monitor conditions close to each worker. Fixed nodes extend environmental coverage through the mine. Both feed a local gateway for logging and supervision, while node-level threshold checks support alarms during a gateway connection loss.

| Capability | Proposed behavior |
| --- | --- |
| Hazard monitoring | Sample CH4, CO, and H2S; extend sensing to dust and runoff quality as those subsystems are defined. |
| Worker warnings | Trigger local buzzer/vibration alerts and display warnings when configured thresholds are crossed. |
| Emergency signaling | Send a manual panic event or an automatic man-down event after sustained inactivity. |
| Underground localization | Associate workers with nearby node zones on a mapped tunnel layout; retain last-seen information. |
| Offline supervision | Run the MQTT broker, rules, monitoring interface, and logs on an on-site Raspberry Pi. |
| Fault visibility | Flag missing nodes, stale packets, sensor faults, and low-power conditions. |

The submission also proposes airflow-aware leak-source estimation and early anomaly detection. These require ventilation measurements, calibration data, and validation beyond the current CAD model.

## System architecture

The diagram summarizes the proposed data flow in the submission. It does not represent software already included in this repository.

```mermaid
flowchart TD
    subgraph underground[Underground sensing]
        gases["Gas sensors: CH4 / CO / H2S"]
        distress["Motion sensor + panic button"]
        helmet["Helmet node / ESP32-C3<br/>Threshold checks + timestamps"]
        fixed["Fixed environmental nodes<br/>Gas / planned dust and runoff sensing"]
        local["Local worker alert<br/>Buzzer / vibration / display"]
        gases --> helmet
        distress --> helmet
        helmet --> local
    end

    helmet --> network["Local wireless network<br/>Wi-Fi + MQTT / proposed mesh"]
    fixed --> network
    network --> gateway["Raspberry Pi 4<br/>Mosquitto MQTT broker"]
    gateway --> rules["Threshold rules + health checks<br/>Timestamp validation"]
    rules --> logs["Offline telemetry logs"]
    rules --> supervisor["Supervisor interface<br/>OLED / siren / alerts"]
    rules --> zones["Tunnel map + node zones<br/>Worker last-seen status"]
    gateway -->|"Warnings over the local network"| helmet
```

1. A node captures sensor readings and attaches a timestamp and node identity.
2. The controller checks local alarm conditions and sends telemetry over the local network.
3. The gateway validates incoming data, applies rules, and records readings offline.
4. Supervisors receive hazard and node-health information; worker positions are associated with mapped zones.

Wi-Fi/MQTT is the baseline communication design. Multi-hop routing, Kinetic Mesh, and alternative radio fallbacks appear in the submission as proposed extensions; their implementation and underground coverage remain to be demonstrated.

## Hardware and software design

| Subsystem | Selection or role described in the submission |
| --- | --- |
| Node controller | ESP32-C3 for sensor acquisition, threshold checks, timestamps, and wireless telemetry. |
| Methane sensing | MQ-4 sensor, subject to calibration and heater-power validation. |
| Carbon monoxide sensing | MQ-7 sensor, with its sampling and heater cycle to be validated. |
| Hydrogen sulfide sensing | Electrochemical H2S sensor with analog signal conditioning; final sensor part is unspecified. |
| Temperature/humidity | A sensor is represented in the supplied CAD assembly; compensation is discussed in the risk-mitigation plan. |
| Motion and panic input | Motion sensing for man-down detection and a manual distress button; final parts are unspecified. |
| Dust and runoff sensing | Included in project scope; sensor models, interfaces, and calibration methods remain to be selected. |
| Node power | Proposed 3.7 V, 2500 mAh LiPo, charging/protection, and regulated supply rails. |
| Local gateway | Raspberry Pi 4 Model B, 4 GB RAM, with Mosquitto MQTT and local processing. |
| Storage and outputs | Proposed 64 GB microSD logging, 1.3-inch OLED, and an 85 dB siren/alarm output. |
| Mechanical design | Enclosure, lid, mounting standoffs, board placement, and wiring represented in the STEP assembly. |

The STEP model is a mechanical presentation of one sensor pod. Its generic component geometry does not establish exact electronic part numbers or demonstrate the complete helmet, gateway, or multi-node installation.

## Engineering targets

These targets come from the project specification on page 7 of the [Stage 2 submission](docs/stage-2-submission.pdf). They have not been verified by measurements in this repository.

| Parameter | Design target |
| --- | --- |
| Gas sampling | 1 Hz for CH4, CO, and H2S |
| End-to-end gas alert | Less than 10 seconds between threshold crossing and helmet warning |
| Battery endurance | 8 hours on a 3.7 V, 2500 mAh LiPo |
| Average node power | Approximately 1 W, with sensor-heater duty cycling proposed |
| Wearable pod envelope | Approximately 52 × 88 × 28 mm and 120 g; a target, not a measured property of the supplied STEP file |
| Ingress protection | IP67 target; no ingress-test evidence supplied |
| Offline logging | At least 7 days at the local gateway |
| Missing-node detection | Flag a node within 30 seconds of lost contact |
| Man-down detection | Trigger after 30 seconds without motion |
| Worker localization | Nearest-node zone on a mapped tunnel network |

## CAD and design evidence

The three supplied screenshots retain the CAD application's component browser and workspace. They show the enclosure arrangement and assembly structure at the time of capture.

| Assembly overview | Enclosure and component tree |
| --- | --- |
| [![Assembly overview with the lid raised above the sensor enclosure](assets/cad/assembly-overview.jpeg)](assets/cad/assembly-overview.jpeg) | [![CAD component browser showing enclosure, standoffs, controller, and sensor components](assets/cad/enclosure-components.jpeg)](assets/cad/enclosure-components.jpeg) |
| Board placement, gas-sensor module, internal wiring, and exploded lid. | Enclosure and mounting components visible alongside the assembly. |

The full-width image near the top shows the wiring in greater detail. Open any screenshot to inspect it at its original resolution.

### Download and inspect the model

- [Download VKA2026.step](https://github.com/SrivarsanK/PranRakshak/raw/refs/heads/main/cad/VKA2026.step)
- [Browse the model in this repository](cad/VKA2026.step)
- [Read the CAD component guide and provenance notes](cad/README.md)

Clone the repository to keep the model and its documentation together:

```bash
git clone https://github.com/SrivarsanK/PranRakshak.git
cd PranRakshak
```

Import `cad/VKA2026.step` into a STEP-compatible CAD application such as Fusion, FreeCAD, or SolidWorks. Units are millimetres. With the lid in its exploded position, inspect the enclosure, component placement, standoffs, and wiring.

The supplied file is a STEP assembly exchange model. The originating application's editable sketches and parametric feature history are separate deliverables and are not included here.

## Safety and reliability plan

The submission describes the following protections for implementation and testing:

| Failure condition | Planned response |
| --- | --- |
| Sensor drift, failure, or a stuck reading | Calibration checks, plausibility checks, and an explicit sensor-fault alert. |
| Node loses its gateway connection | Continue local threshold alarms; retry communication and flag the missing node at the gateway. |
| Stale or clock-skewed telemetry | Timestamp packets and reject stale data before localization; the FMEA proposes a 10-second cutoff. |
| Low battery or brownout | Monitor supply state, issue a low-power warning, and test watchdog/reset behavior. |
| Gateway failure | Preserve node-level alarms and identify loss of central monitoring. |
| Ventilation changes or poor node placement | Update the tunnel map and airflow assumptions, then repeat localization tests. |

Intrinsic safety, flame protection, enclosure sealing, and impact resistance require further engineering and test evidence. No mining-equipment certification is claimed by the materials in this repository.

## Roadmap

The schedule below follows the submission's October 2026–January 2027 fabrication plan. Items remain open until supporting deliverables are published.

| Period | Planned work | Evidence to publish |
| --- | --- | --- |
| October 2026 | Finalize schematics, run electrical checks, procure components, and bench-calibrate gas sensors. | Editable EDA files, check reports, BOM, and calibration records. |
| November 2026 | Assemble four sensor nodes and the helmet unit; bring up the Pi gateway, broker, display, and alarms. | Assembly photos, firmware, gateway configuration, and timestamped telemetry. |
| December 2026 | Test connectivity, node loss, man-down detection, watchdogs, brownouts, and corridor localization. | Integration logs and measured alert/localization behavior. |
| January 2027 | Run endurance and drift tests, tune the system, and prepare the Stage 3 demonstration. | Battery measurements, soak-test records, and demonstration evidence. |

## Repository contents

```text
PranRakshak/
├── README.md
├── assets/
│   ├── pran-rakshak-banner.svg
│   └── cad/
│       ├── assembly-wiring.jpeg
│       ├── assembly-overview.jpeg
│       └── enclosure-components.jpeg
├── cad/
│   ├── README.md
│   └── VKA2026.step
└── docs/
    ├── design-notes.md
    └── stage-2-submission.pdf
```

For the evidence inventory, source-page mapping, and unresolved specification details, see [design notes](docs/design-notes.md).

## Team and submission

| Field | Details |
| --- | --- |
| Project | PRAN RAKSHAK |
| Team | Codemium |
| Team leader | Kaaviya Varshini V |
| Team ID | VK26-IITH-SM-0275 |
| Event | Vishwakarma Awards 2026–27, Stage 2 |
| Theme | Theme 5: Sustainable Mining — Worker Health, Safety & Environmental Hazard Tracking |

## Sources and acknowledgements

The team's [Stage 2 submission PDF](docs/stage-2-submission.pdf) supplies the project scope and specifications; the CAD screenshots and STEP model document the supplied design. Template examples are excluded as evidence of completed work.

The README's visual organization takes inspiration from [REACH by dmunish](https://github.com/dmunish/reach#readme).
