---
name: ark-geospatial-ai
description: Use when applying deep learning or machine learning to geospatial data, including satellite image classification, object detection, segmentation, or GeoAI workflows.
triggers:
  - geospatial AI
  - GeoAI
  - satellite classification
  - object detection satellite
  - segmentation geospatial
  - torchgeo
  - deep learning GIS
  - land cover classification
role: specialist
scope: implementation
output-format: code
---

# Geospatial AI & Deep Learning

Machine learning and deep learning for satellite imagery analysis and spatial pattern recognition.

## Core Libraries

| Library | Purpose | Models |
|---------|---------|--------|
| **GeoAI** | Unified GeoAI framework | SAM, YOLO, segmentation |
| **torchgeo** | PyTorch geospatial | Pre-trained models, datasets |
| **segment-geospatial** | SAM for geo | Interactive segmentation |
| **rasterio** | Raster I/O | Data loading |
| **rastervision** | ML pipelines | Training workflows |
| **solaris** | Overhead imagery | Building/road extraction |

## Installation

```bash
pip install geoai torchgeo segment-geospatial rastervision
pip install torch torchvision  # PyTorch backend
```

## Pre-trained Models

| Model | Task | Source |
|-------|------|--------|
| **SAM** | Segmentation | Meta AI |
| **ResNet/EfficientNet** | Classification | torchgeo |
| **U-Net** | Semantic segmentation | torchgeo |
| **YOLO** | Object detection | Ultralytics |
| **Prithvi** | Foundation model | IBM/NASA |

## Common Tasks

### Land Cover Classification
- Urban/vegetation/water mapping
- Crop type identification
- Forest monitoring
- Change detection

### Object Detection
- Building footprints
- Vehicle counting
- Ship detection
- Infrastructure mapping

### Segmentation
- Field boundary extraction
- Road network mapping
- Flood extent delineation
- Solar panel detection

## GeoAI Workflow

```python
from geoai import download_image, segment_image

# Download satellite tile
image = download_image(bbox, source="sentinel-2")

# Segment with SAM
masks = segment_image(image, model="sam")

# Export results
masks.to_file("segmentation.gpkg")
```

## Training Data

| Dataset | Type | Size |
|---------|------|------|
| SpaceNet | Buildings | 27 cities |
| UC Merced | Classification | 21 classes |
| EuroSAT | Classification | 27,000 patches |
| xView | Detection | 1M objects |
| DOTA | Detection | Aerial images |

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| torchgeo | `references/torchgeo.md` | PyTorch workflows |
| SAM | `references/segment-anything.md` | Interactive segmentation |
| Training | `references/training-data.md` | Dataset preparation |
| Inference | `references/inference.md` | Model deployment |

## Constraints

### MUST DO
- Use appropriate image normalization
- Split data geographically (no leakage)
- Validate with held-out regions
- Consider class imbalance

### MUST NOT DO
- Train without augmentation
- Ignore spatial autocorrelation
- Use RGB-only when bands available
- Skip post-processing (CRF, morphology)
