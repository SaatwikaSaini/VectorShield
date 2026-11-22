# VectorShield: Biometric Template & Presentation Attack Simulator

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.2x-orange.svg)](https://numpy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An educational biometric security sandbox designed to demonstrate template vector extraction, Euclidean distance matching verification, and systemic vulnerabilities to presentation attacks (spoofing). **VectorShield** downnsamples facial regions into a localized 10-dimensional spatial array to simulate authentication pipelines and test verification boundaries.

---

## Table of Contents
- [Overview](#overview)
- [Core Mathematical Concepts](#core-mathematical-concepts)
- [Key Features](#key-features)
- [Project Architecture](#project-architecture)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [License](#license)

---

## Overview

Modern biometric verification relies heavily on converting biological structures into mathematical coordinate spaces. **VectorShield** acts as an interactive simulation environment to explore how templates are compiled, registered, and validated. By introducing intentional "Spoof" commands, the project maps out security vulnerabilities, helping developers visualize why pure spatial templates require secondary heuristic checking layers (like liveness tracking).

---

## Core Mathematical Concepts

### 1. Feature Extraction Spatial Mapping
To form a predictable template, the localized face region of interest (ROI) is flattened into a predictable structure. The system downsamples input matrices to a strict $5 \times 2$ grid layout. Normalizing grayscale pixel intensities ($[0, 255]$) down to a continuous floating-point range ($[0.0, 1.0]$) yields an exact 10-dimensional spatial array representing structural light distributions:

$$\vec{v} \in \mathbb{R}^{10}$$

### 2. Biometric Distance Verification
Verification is assessed by calculating the spatial proximity between a freshly captured input vector ($\vec{v}_{\text{captured}}$) and a baseline enrolled record vector ($\vec{v}_{\text{stored}}$). The application employs a standard Euclidean distance metric (L2 Norm):

$$\text{dist} = \| \vec{v}_{\text{stored}} - \vec{v}_{\text{captured}} \|_2 = \sqrt{\sum_{i=1}^{10} (v_{\text{stored}, i} - v_{\text{captured}, i})^2}$$

Authentication is granted only if the distance score falls below a strict predefined threshold. ($\text{dist} < \epsilon$).

---

## Key Features

- **10-D Vector Representation:** Real-time spatial array extraction from localized regions of interest.
- **Biometric Matching Engine:** Precise structural calculation using floating-point matrix distance evaluations.
- **Security Vulnerability Sandbox:** Built-in testing hooks to simulate presentation attacks and log boundary breaches.
- **Clean Object Architecture:** Decoupled layout separating hardware frame reading from verification calculations.

---

## Project Architecture

```text
vectorshield/
├── core/
│   ├── __init__.py
│   ├── config.py        # Centralized thresholds & spatial shapes
│   └── engine.py        # High-performance vector math & database handling
├── app.py               # Asynchronous video engine & UI console
├── .gitignore
├── LICENSE
└── README.md
