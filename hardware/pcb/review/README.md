# PCB integration review

[Board guide](../README.md) · [Native DRC JSON](DRC_Report.json) · [KiCad layer export](PCB_Layers.svg)

The standalone board supplied in the PCB ZIP was reviewed with KiCad 10.0.7 on 25 October 2026. No source-board edits were made. The native board file still matches the original archive and downloaded board byte for byte.

## Review conditions

The package contains no `.kicad_pro` or matching `.kicad_sch`. DRC therefore used the standalone board's effective default settings. All severity levels and all track errors were requested. Zones were refilled in memory, without `--save-board`; schematic parity was not requested because no matching schematic was supplied. Five checks remain ignored under the effective defaults, as recorded in the JSON report.

From the repository root, the check was run as follows:

```bash
kicad-cli pcb drc --format json --severity-all --all-track-errors --refill-zones --exit-code-violations --output hardware/pcb/review/DRC_Report.json hardware/pcb/PRAN_RAKSHAK_RevA.kicad_pcb
```

The command returned nonzero because findings remain.

## Results

| Category | Count |
| --- | --- |
| Rule violations | 61: 5 errors and 56 warnings |
| Unconnected items | 33, reported separately as errors |
| Incomplete thermal-relief connections | 5 errors |
| Footprint-library review issues | 49 warnings |
| Text height, silkscreen overlap, silkscreen over copper, and back-layer text orientation | 7 warnings combined |

These are findings for the separate PCB carrier draft. The earlier four-sheet schematic's ERC result applies to that schematic only. The PCB is not a passed DRC design or a demonstrated schematic match.

## Native layer export

`PCB_Layers.svg` was exported from the stored board with F.Cu, B.Cu, F.SilkS, and Edge.Cuts selected. Export succeeded without modifying the original board. It illustrates the stored routing and placement; it is not a fabrication release or proof of complete connectivity.
