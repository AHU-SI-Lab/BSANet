# BSANet
# GH-PGD v1.0

**GH-PGD** is an annotation-oriented benchmark dataset for fine-grained plastic greenhouse (PG) mapping from very high-resolution (VHR) remote sensing imagery.

It accompanies the manuscript:

**Fine-Grained Mapping of Plastic Greenhouses from Very High-Resolution Remote Sensing Imagery: A Global Benchmark and Boundary-Guided Separation-Aware Network**

The original VHR image patches are **not redistributed** because the source imagery was obtained from Google Earth and is subject to imagery-provider licensing restrictions. This release provides annotation masks and patch-level geographic metadata.

---

## Overview

GH-PGD is designed to support fine-grained plastic greenhouse mapping, dense-scene separation, and object-level structural analysis.

### Dataset at a glance

- **Task**: Plastic greenhouse mapping from VHR remote sensing imagery
- **Release type**: Annotation-oriented release
- **Patch size**: 512 × 512
- **Total patches**: 32,556
- **Training patches**: 16,278
- **Validation patches**: 8,139
- **Test patches**: 8,139
- **Greenhouse instances**: 159,175
- **Study areas**: 14 representative PG regions
- **Geographic coverage**: Asia, Europe, and Africa
- **Countries**: China, Turkey, Algeria, Palestine, Syria, and Italy
- **Annotations**:
  - Pixel-level semantic masks
  - Object-level instance masks
  - COCO-style JSON annotation files
- **Geographic metadata**:
  - Patch-level geographic indices
  - Patch-level geographic extents

---

## Directory Structure

```text
GH-PGD_v1.0/
├── README.md
├── LICENSE
├── metadata/
│   ├── patch_index.csv
│   ├── patch_extents.geojson
│   └── instance_summary.csv
└── annotations/
    ├── semantic_masks/
    │   ├── train/
    │   ├── val/
    │   └── test/
    ├── instance_masks/
    │   ├── train/
    │   ├── val/
    │   └── test/
    └── coco_json/
        ├── train.json
        ├── val.json
        └── test.json
```

---

## Released Materials

### 1. Semantic masks

Semantic masks are stored in:

```text
annotations/semantic_masks/
```

The masks are binary annotation masks:

```text
0 = background or non-target region
1 = plastic greenhouse
```

### 2. Instance masks

Instance masks are stored in:

```text
annotations/instance_masks/
```

The instance masks use integer IDs:

```text
0 = background
1, 2, 3, ... = individual plastic greenhouse instances
```

Each instance mask corresponds to a semantic mask with the same patch ID.

### 3. COCO-style annotation files

COCO-style JSON annotation files are stored in:

```text
annotations/coco_json/
```

These files provide object-level annotation information for the train, validation, and test splits.

### 4. Patch-level metadata

Patch-level metadata are stored in:

```text
metadata/
```

The main metadata files are:

| File | Description |
|---|---|
| `patch_index.csv` | Patch ID, split, study area, row/column index, pixel window, geographic bounds, and annotation file paths |
| `patch_extents.geojson` | Patch-level polygon extents in WGS84 / EPSG:4326 |
| `instance_summary.csv` | Patch-level statistics of object-level annotations |

---

## Dataset Splits

| Split | Number of patches |
|---|---:|
| Train | 16,278 |
| Validation | 8,139 |
| Test | 8,139 |
| **Total** | **32,556** |

---

## Tasks and Benchmarks

GH-PGD can support the following tasks:

### 1. Semantic segmentation

- **Goal**: Extract plastic greenhouse coverage.
- **Annotations**: Semantic masks.
- **Example metrics**: IoU, mIoU, Precision, Recall, F1-score.

### 2. Boundary-aware mapping

- **Goal**: Evaluate boundary quality and separation of adjacent greenhouses.
- **Annotations**: Semantic masks and derived boundary labels.
- **Example metrics**: Boundary IoU, ASSD, HD95.

### 3. Object-level structural analysis

- **Goal**: Analyze greenhouse instances, density, shape, and spatial organization.
- **Annotations**: Instance masks and COCO-style object annotations.
- **Example metrics**: Object count consistency, greenhouse under-segmentation, dense-scene separation quality.

---

## Image Availability

This release does **not** include:

- Google Earth source imagery;
- original large GeoTIFF images;
- quadrant GeoTIFF images;
- 512 × 512 RGB image patches;
- any `images/` folder.

The released dataset is annotation-oriented. Users who need image patches should obtain corresponding imagery from authorized sources using the released patch-level geographic extents and comply with the applicable imagery-provider terms of use.

The released `patch_index.csv` and `patch_extents.geojson` define the exact set of GH-PGD patches. Image reconstruction, if needed, should follow these patch-level extents.

---

## Code

The BSANet model code is available at:

```text
https://github.com/AHU-SI-Lab/BSANet
```

---

## License

The released GH-PGD annotation-oriented materials are provided for academic and non-commercial research use.

This license applies only to the released annotation-oriented materials, including semantic annotation masks, instance masks, COCO-style JSON annotation files, patch-level geographic indices, patch-level geographic extents, metadata files, and related documentation.

This release does not include Google Earth imagery or derived RGB image patches. Such imagery is not redistributed and remains subject to the terms of use and licensing restrictions of the corresponding imagery providers.

---

## Citation

If you use GH-PGD, please cite the accompanying manuscript:

```text
Fine-Grained Mapping of Plastic Greenhouses from Very High-Resolution Remote Sensing Imagery:
A Global Benchmark and Boundary-Guided Separation-Aware Network.
```

A formal citation will be updated after publication.

---

## Contact

For questions about the dataset, annotations, or code, please contact the corresponding author of the accompanying manuscript.
