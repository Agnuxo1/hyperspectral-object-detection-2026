# Hyperspectral Object Detection Challenge 2026

![Hyperspectral detector header](assets/header.png)

An open-source, reproducible reference pipeline for [Hyperspectral Object Detection Challenge 2026](https://www.kaggle.com/competitions/hyperspectral-object-detection-challenge-2026). The design keeps all 16 visible-light bands (460–600 nm), predicts 18 classes, and targets the official `mAP@[0.50:0.95]` metric.

![Spectral cube and signatures](assets/spectral-cube.png)

## Design

```text
H x W x 16 cube -> train-only band normalization
    -> spectral stem -> CSP/FPN/PAN detector -> class-wise NMS
    -> optional TTA from the same network -> submission.csv
```

The spectral stem uses a 1x1 projection followed by spatial convolutions so pretrained RGB features can be inflated without silently discarding spectral information. The pseudo-RGB route remains a control experiment only.

![Tile inference](assets/tile-inference.png)

## Experiment ladder

1. `E0`: pseudo-RGB detector for labels, boxes, and submission-contract checks.
2. `E1`: 16-band detector with an inflated RGB initialization.
3. `E2`: spectral dropout, per-band intensity jitter, and spatial augmentation.
4. `E3`: high-resolution or tiled inference, selected only when a subject-safe validation split improves.

![Evaluation view](assets/evaluation.png)

## Reproducibility and rules

Competition data and generated weights are excluded from this public release. Use only data and pretrained models permitted by the current rules, record their sources and licenses, and validate the exact `submission.csv` schema. A local score is not evidence of real-world remote-sensing performance.

## License

MIT for the original code. See [LICENSE](LICENSE). External datasets, pretrained backbones, and dependencies retain their own licenses.
