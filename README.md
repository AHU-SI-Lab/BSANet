# BSANet and GH-PGD v1.0

Official repository for the **Boundary-Guided Separation-Aware Network (BSANet)** and the **GH-PGD v1.0** benchmark dataset for fine-scale plastic greenhouse (PG) mapping from very high-resolution (VHR) remote sensing imagery.

This repository accompanies the manuscript:

**Fine-Scale Mapping of Plastic Greenhouses from Very High-Resolution Remote Sensing Imagery: A Global Benchmark Dataset and Boundary-Guided Separation-Aware Network**

The BSANet model implementation is maintained in this GitHub repository.  
The formal GH-PGD v1.0 dataset release is archived on **Zenodo**.

---

## Overview

GH-PGD (Global High-Resolution Plastic Greenhouse Dataset) is an annotation-oriented benchmark dataset designed for:

- fine-scale plastic greenhouse mapping;
- dense-scene greenhouse separation;
- boundary-aware segmentation;
- object-level structural analysis;
- cross-region and cross-domain evaluation.

The annotations were produced in the context of VHR RGB remote-sensing imagery accessed through Google Earth.

Because of source-imagery licensing restrictions, the original RGB imagery and derived RGB image patches are **not redistributed**.

---

## Dataset Download

The formal GH-PGD v1.0 release is available on Zenodo:

**Dataset DOI:**  
https://doi.org/10.5281/zenodo.22929049

**Zenodo record:**  
https://zenodo.org/records/22929049

The Zenodo release should be regarded as the authoritative archived version of GH-PGD v1.0.

---

## Dataset at a Glance

| Item | Value |
|---|---:|
| Version | v1.0 |
| Countries | 9 |
| Study areas | 16 |
| Sub-regions | 18 |
| Total patches | 37,732 |
| Training patches | 18,866 |
| Validation patches | 9,433 |
| Test patches | 9,433 |
| Patch size | 512 × 512 |
| Nominal spatial resolution | 0.5 m |
| Patch-level instance annotations | 198,247 |

GH-PGD covers study areas in:

- China
- Turkey
- Algeria
- Palestine
- Syria
- Italy
- Australia
- Argentina
- Mexico

across Asia, Europe, Africa, Oceania, North America, and South America.

---

## Released Dataset Materials

The formal Zenodo release provides:

- semantic masks;
- instance masks;
- instance-level annotations;
- fixed train/validation/test splits;
- patch-level geographic metadata;
- acquisition dates;
- geographic extents;
- source-image valid footprints;
- dataset documentation;
- metadata schema;
- quality-control report;
- release validation script.

The formal dataset structure is:

```text
GH-PGD_v1.0/
├── README.md
├── LICENSE.md
├── CHANGELOG.md
├── VERSION.txt
├── CITATION.cff
├── final_public_metadata_schema.md
├── FINAL_QC_REPORT.md
├── validate_ghpgd_release.py
├── splits/
│   ├── train.txt
│   ├── val.txt
│   └── test.txt
├── semantic_masks/
│   ├── train/
│   ├── val/
│   └── test/
├── instance_masks/
│   ├── train/
│   ├── val/
│   └── test/
├── annotations/
│   ├── instance_annotations.json
│   └── instance_statistics.csv
├── metadata/
│   ├── patch_metadata.csv
│   ├── study_area_metadata.csv
│   ├── source_imagery_metadata.csv
│   ├── geographic_extents.geojson
│   └── source_image_valid_footprints.geojson
└── documentation/
    ├── dataset_structure.md
    ├── annotation_definition.md
    └── image_reconstruction_guide.md
```

For complete dataset documentation, metadata definitions, quality-control information, and reconstruction guidance, please refer to the README and documentation included in the Zenodo release.

---

## Dataset Splits

| Split | Number of patches | Instance annotations |
|---|---:|---:|
| Train | 18,866 | 106,051 |
| Validation | 9,433 | 46,098 |
| Test | 9,433 | 46,098 |
| **Total** | **37,732** | **198,247** |

The predefined partitions are mutually exclusive and jointly contain all released patch IDs.

---

## Image Availability

The GH-PGD v1.0 public release does **not** redistribute:

- original Google Earth VHR imagery;
- original VHR GeoTIFF imagery;
- derived 512 × 512 RGB image patches;
- visualization products containing source RGB imagery.

The public release contains only redistributable author-created annotations, masks, metadata, geographic extents, acquisition metadata, documentation, and validation materials.

Users who need corresponding RGB imagery should obtain imagery from authorized sources and comply with the applicable imagery-provider terms of use.

The released geographic footprints, acquisition dates, imagery attribution information, and nominal 0.5 m spatial resolution can be used as spatial references for preparing authorized imagery corresponding to the annotations.

---

## Model Code

The BSANet implementation is provided in this repository under:

```text
Model/
```

BSANet is designed for fine-scale plastic greenhouse extraction in dense agricultural scenes.

The network incorporates boundary information into semantic feature learning to improve the separation of adjacent greenhouse objects and reduce object adhesion.

The model is evaluated using pixel-level, boundary-level, and object-level metrics.

---

## Main Tasks

GH-PGD can support several research tasks.

### 1. Semantic Segmentation

**Goal:** Extract plastic greenhouse coverage.

Typical metrics include:

- IoU
- Precision
- Recall
- F1-score

### 2. Boundary-Aware Segmentation

**Goal:** Evaluate greenhouse boundary quality and the separation of adjacent PG objects.

Typical metrics include:

- Boundary IoU
- HD95
- MED2

### 3. Object-Level Analysis

**Goal:** Evaluate object integrity, separation, and greenhouse counting performance.

The released instance masks and instance annotations can also support research on greenhouse size, density, spatial organization, and instance-level structure.

---

## Quality Control

The formal GH-PGD v1.0 release passed the complete release validation reported in `FINAL_QC_REPORT.md`.

Key validated quantities include:

- 37,732 semantic masks;
- 37,732 instance masks;
- 198,247 instance annotations;
- 37,732 valid patch-level geographic footprints;
- 18 valid source-image footprints;
- complete acquisition dates for all released sub-regions;
- mutually exclusive train/validation/test partitions.

The validation script `validate_ghpgd_release.py` is included in the Zenodo release.

---

## License

The BSANet source code in this repository is released under the MIT License.

The GH-PGD v1.0 dataset is released separately on Zenodo under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

The GH-PGD license applies only to the released author-created annotations, masks, metadata, and documentation and does not grant rights to the underlying third-party source imagery.

## Citation

If you use GH-PGD v1.0, please cite the dataset:

```text
Wang, Y., Zhang, P., Wu, Y., Yang, H., Wang, B., Wang, C., Zhang, X., & Du, P.
GH-PGD: Global High-Resolution Plastic Greenhouse Dataset (Version 1.0) [Data set].
Zenodo.
https://doi.org/10.5281/zenodo.22929049
```

If you use BSANet or the benchmark results, please also cite the accompanying manuscript:

```text
Fine-Scale Mapping of Plastic Greenhouses from Very High-Resolution Remote Sensing Imagery:
A Global Benchmark Dataset and Boundary-Guided Separation-Aware Network.
```

The formal manuscript citation will be updated after publication.

---

## Version

GH-PGD v1.0 is the first formally versioned release corresponding to the associated manuscript.

Earlier dataset materials previously hosted through this GitHub repository represented development-stage contents and should not be treated as the formal GH-PGD v1.0 release.

For reproducibility, please use the archived Zenodo release associated with:

```text
DOI: 10.5281/zenodo.22929049
```

---

## Contact

For questions regarding GH-PGD, BSANet, annotations, metadata, or model implementation, please contact the corresponding author of the accompanying manuscript.
