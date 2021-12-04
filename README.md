[![author](https://img.shields.io/badge/author-felipehonorato1-yellow.svg)](https://github.com/felipehonorato1)
[![author](https://img.shields.io/badge/author-francisccdn-blue.svg)](https://github.com/francisccdn) 
[![author](https://img.shields.io/badge/author-humbertonc-red.svg)](https://github.com/humbertonc) 
[![author](https://img.shields.io/badge/author-laradicp-pink.svg)](https://github.com/laradicp) 
[![author](https://img.shields.io/badge/author-lucenalarissa-green.svg)](https://github.com/lucenalarissa)

# Mask Detection

Use of YOLOv5 for mask detection with notification via Telegram.

<p align="center">
    <img src="example" width="400">
</p>


## Table of Contents
- [About The Project](#about-the-project)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)


## About The Project

In the middle of a pandemic our team was thinking how uncomfortable it is to be indoors with people you don't live with and they don't wear a face mask.Therefore, we decided to make a mask detection project using [YOLOv5](https://github.com/ultralytics/yolov5) and associate it with the Telegram bot as a way to notify the non-use of the mask.


## Getting Started

Instructions for use this repository:

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Felipehonorato1/mask_detection.git
   ```
2. Install packages
   ```sh
   pip install requirements.txt
   ```


### Usage

```sh
cd yolov5/
python detect.py --weights runs/train/exp/weights/best.pt --source 0  --img-size 640 --conf-thres 0.25 --iou-thres 0.45 --device cpu --hide-labels --hide-conf
```
