# Installation Guide

This document provides instructions for installing and setting up the Stock Price Deep Reasoner with Deep Research system.

## Prerequisites

Before installing the system, make sure you have the following prerequisites:

- Python 3.8 or higher
- CUDA-compatible GPU (recommended for vLLM)
- Git (for cloning the repository)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/jihun-yoon/SPDR.git
cd spdr
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Using venv
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory with your configuration: 