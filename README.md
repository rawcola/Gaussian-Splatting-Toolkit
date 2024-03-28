# Gaussian Splatting Toolkit 🛠️

The Gaussian Splatting Toolkit is a cutting-edge collection of tools designed for new view synthesis using Gaussian splatting techniques, providing a novel explicit 3D representation for scene rendering.

## Table of Contents 📖

<details>
  <summary>Table of Content</summary>
  - [Gaussian Splatting Toolkit 🛠️](#gaussian-splatting-toolkit-️)
    - [Table of Contents 📖](#table-of-contents-)
    - [Introduction 🎉](#introduction-)
    - [Features 🌟](#features-)
    - [Installation 💻](#installation-)
    - [Usage 🚀](#usage-)
      - [Download the opensource datasets](#download-the-opensource-datasets)
      - [Data processing](#data-processing)
      - [Train the Gaussian Splatting](#train-the-gaussian-splatting)
      - [Visualize the result](#visualize-the-result)
      - [Render the rgb and depth](#render-the-rgb-and-depth)
      - [Export](#export)
    - [Contribute 🤝](#contribute-)
    - [License 📄](#license-)
    - [Citation 📚](#citation-)
    - [TODO 📝](#todo-)
</details>

## Introduction 🎉

A Gaussian Splatting Toolkit for robotics research, developed based on nerfstudio.

## Features 🌟

- **Explicit 3D Representation:** Utilizes Gaussian splatting for a novel approach to scene rendering.
- **New View Synthesis:** Advanced tools for synthesizing new views from existing data.
- **Data Processing:** Comprehensive data processing capabilities for video and image inputs.
- **Training and Evaluation:** Robust training and evaluation modules for Gaussian Splatting models.
- **Rendering:** High-quality rendering of RGB and depth from various camera poses.
- **Exporting:** Ability to export gaussians, point clouds, camera poses, and TSDFs for further analysis.

## Installation 💻

Using conda:

```bash
conda create -n gstk python=3.10.13 -y
conda activate gstk
pip install torch torchvision
pip install -e .
```

This repository also provides a devcontainer for your convenience.

## Usage 🚀

### Download the opensource datasets

```bash
gs-download-data gstk --save-dir /path/to/save/dir --capture-name all
```

### Data processing

```bash
# Extract from video
gs-process-data video --data /path/to/video --output-dir /path/to/output-dir --num-frames-target 1000
# Extract from images
gs-process-data images --data /path/to/rgb/folder --output-dir /path/to/output-dir
# Extract with both rgb and depth
gs-process-data images --data /path/to/rgb/folder --depth-data /path/to/depth/folder --output-dir /path/to/output-dir
# Process with mono depth estimation
gs-process-data images --data /path/to/rgb/folder --depth-data /path/to/depth/folder --using-est-depth --output-dir /path/to/output-dir
# Process with mask
gs-process-data images --data /mnt/d/Datasets/object/milk_2/rgb/ --depth-data /mnt/d/Datasets/object/milk_2/depth_est/ --using-est-depth --mask-data /mnt/d/Datasets/object/milk_2/masks/ --output-dir /mnt/d/Datasets/gs-recon/object/milk_mask
```

### Train the Gaussian Splatting

```bash
gs-train gaussian-splatting --data /path/to/processed/data
gs-train depth-gs --data /path/to/processed/data
# Train with mono depth estimation
gs-train depth-gs --data /path/to/processed/data --pipeline.model.use-est-depth True
```

### Visualize the result

```bash
gs-viewer --load-config outputs/path/to/config.yml
```

### Render the rgb and depth

From trajectory

```bash
gs-render trajectory --trajectory-path /path/to/trajectory.json --config-file /path/to/ckpt/config.yml
```

From camera pose

```bash
gs-render pose --config-file /path/to/config.yml --output-dir /path/to/output/folder/
```

### Export

Export the gaussians as ply

```bash
gs-export gaussian-splat --load-config /path/to/config.yml --output-dir exports/gaussians/
```

Export camera poses

```bash
gs-export camera-poses --load-config /path/to/config.yml --output-dir exports/cameras/
```

Export the point cloud

```bash
gs-export point-cloud --load-config /path/to/config.yml --output-dir exports/pcd/
```

```bash
gs-export offline-tsdf --render-path /path/to/rendered/folder --output-dir exports/tsdf/
```

Export tsdf with mask

```bash
gs-export offline-tsdf --render-path /path/to/rendered/folder --output-dir exports/tsdf/ --mask-path /path/to/mask
```

Export object pointcloud and mesh with prompt

```bash
gs-export offline-tsdf --render-path exports/milk/ --output-dir exports/tsdf/milk_text_seg --seg-prompt your.prompt
```

## Contribute 🤝

We welcome contributions from the community! If you have a feature request, bug report, or a new idea, feel free to open an issue or submit a pull request. To add a new submodule, run:

```bash
git subtree add --prefix {local directory being pulled into} {remote repo URL} {remote branch} --squash
```

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation 📚

If you use the Gaussian Splatting Toolkit in your research, please cite it as follows:

```bibtex
@misc{gaussian_splatting_toolkit,
  author = {Your Name},
  title = {Gaussian Splatting Toolkit: A Toolkit for 3D Reconstruction and New View Synthesis},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/H-tr/gaussian-splatting-toolkit}}
}
```

## TODO 📝
- [x] OpenCV marker ground truth measurement.
- [x] Surface distance module
- [ ] Data
  - [ ] Data synthetic with blender
- [ ] Data preprocessing
  - [x] Colmap preprocessing
  - [x] RGB-D Data processing
  - [ ] Sensor interface
    - [ ] Azure Kinect
    - [ ] iPhone/ iPad
- [x] Evaluation
- [x] Gaussian Splatting module
- [x] Depth Loss
- [x] Point cloud export
- [x] Mesh extraction
  - [x] Marching cube
  - [x] TSDF
  - [x] Piossion reconstruction
- [x] Training
  - [x] Course to fine
- [x] Mask
- [ ] Model
  - [ ] Gaussian Splatting SLAM
  - [ ] GaussianShader
- [ ] Visualization
  - [ ] normal visualization
  - [ ] gaussian ellipsoid visualization
  - [ ] pointcloud
  - [ ] mesh
  - [ ] Any gaussians without loading pipeline
  - [ ] mask prompt
  - [ ] segmentation visualization
- [x] Render
  - [x] Render GS model without loading pipeline
- [ ] Documentation
- [ ] Tests
- [x] CUDA
  - [x] migrate the rasterizer to cuda-12.1
