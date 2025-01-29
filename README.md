# Perlin Noise Image Generator

This project generates a 720p image based on Perlin noise. It utilizes Python's capabilities along with the Pillow library for image processing.

## Project Structure

```
perlin-noise-image-generator
├── src
│   ├── main.py
│   └── utils
│       └── perlin_noise.py
├── requirements.txt
└── README.md
```

## Installation

To get started, clone the repository and navigate to the project directory. Then, install the required dependencies using pip:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

To generate a Perlin noise image, run the main script:

```
python src/main.py
```

This will create a 720p image based on Perlin noise and save it in the project directory.

## Dependencies

This project requires the following Python packages:

- numpy
- Pillow

Make sure to have these installed before running the application.