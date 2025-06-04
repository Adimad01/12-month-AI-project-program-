# Image-to-Do

> An AI-powered application that extracts to-do items from images (e.g., handwritten notes, photographs of sticky notes) and organizes them into a structured task list.

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Prerequisites](#prerequisites)  
4. [Installation](#installation)  
5. [Usage](#usage)  
   - [Running the App](#running-the-app)  
   - [Example Workflow](#example-workflow)  
6. [Project Structure](#project-structure)  
7. [Configuration](#configuration)  
8. [Extending the Project](#extending-the-project)  
9. [Troubleshooting](#troubleshooting)  
10. [Contributing](#contributing)  
11. [License](#license)  

---

## Project Overview

**Image-to-Do** is a prototype designed to automatically convert images containing handwritten or printed text—such as sticky notes, whiteboard photos, or printed documents—into a structured to-do list. Using OCR (Optical Character Recognition) and natural language processing, the application:

1. Loads an input image containing tasks.  
2. Applies image preprocessing (e.g., grayscale conversion, noise removal).  
3. Runs an OCR engine (e.g., Tesseract) to extract raw text.  
4. Parses the extracted text to identify individual tasks.  
5. Outputs a JSON or plain-text to-do list with each item on a separate line.

This project demonstrates Week 2 of the 12-Month AI Project Program, focusing on image-based document understanding and task extraction.

---

## Features

- 📷 **Image Preprocessing**: Converts images to grayscale, resizes, and denoises for improved OCR accuracy.  
- 📝 **OCR Integration**: Uses Tesseract (via `pytesseract`) or an alternative OCR engine to extract text from images.  
- 🔍 **Text Parsing**: Identifies task-like sentences or lines (e.g., lines starting with a checkbox indicator like “[]”, “-”, or keywords like “TODO”).  
- ⚙️ **Flexible Input**: Supports common image formats (JPG, PNG) and scanned documents (PDF).  
- 📦 **Output Formats**: Outputs results as a JSON file (`tasks.json`) or a plain-text file (`tasks.txt`).  
- 🔄 **Batch Processing**: Can process multiple images in a directory, generating a combined to-do list.  

---

## Prerequisites

- **macOS, Linux, or Windows**  
- **Python 3.8+** (we recommend 3.9 or 3.10)  
- **Tesseract OCR** installed on your system  
  - macOS: `brew install tesseract`  
  - Ubuntu/Linux: `sudo apt-get install tesseract-ocr`  
  - Windows: Download installer from [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract)  
- Python libraries (see `requirements.txt`)  
- Git (to clone the repository)  

---

## Installation

1. **Clone this repository** (if you haven’t already):
   ```bash
   git clone https://github.com/Adimad01/12-month-AI-project-program-.git
   cd 12-month-AI-project-program-/
   git checkout 443cbbf54584ab56a3822b0c4756d7e1bb3a4d5f
   cd "Month 1/Week 2/Image-to-Do"
   ```

2. **Create and activate a Python virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   > If you don’t have a `requirements.txt`, you can install directly:
   > ```bash
   > pip install pillow opencv-python pytesseract numpy
   > ```

4. **Verify Tesseract installation**:
   ```bash
   tesseract --version
   ```
   You should see Tesseract’s version information. If not, revisit [Tesseract installation instructions](https://github.com/tesseract-ocr/tesseract).

---

## Usage

### Running the App

With your virtual environment activated, run the main script. For example, if your entry point is `main.py`:

```bash
python main.py --image path/to/your/image.jpg --output tasks.json
```

- `--image`: Path to the input image (JPG, PNG, etc.).  
- `--output`: (Optional) Path to the JSON file where tasks will be saved. If omitted, `tasks.json` is created in the current directory.

You can also process an entire folder:

```bash
python main.py --input_dir path/to/images/ --output tasks_combined.json
```

### Example Workflow

1. Place `example.jpg` (a photo of handwritten notes) in the folder.  
2. Run:
   ```bash
   python main.py --image example.jpg
   ```
3. Check the generated `tasks.json`, which might look like:
   ```json
   {
     "tasks": [
       "Buy groceries",
       "Call Alice about the meeting",
       "Finish the draft report",
       "Book flight tickets"
     ]
   }
   ```
4. Open `tasks.txt` (generated alongside) to see a plain-text list:
   ```
   - Buy groceries
   - Call Alice about the meeting
   - Finish the draft report
   - Book flight tickets
   ```

---

## Project Structure

```
Image-to-Do/
├── .venv/                   # (gitignored) Python virtual environment
├── data/                    # Sample images for testing
│   ├── example_1.jpg
│   └── example_2.png
├── outputs/                 # Generated outputs (tasks.json, tasks.txt)
├── src/                     # Source code
│   ├── main.py              # Entry point / CLI interface
│   ├── ocr_utils.py         # Functions for loading and preprocessing images
│   ├── parse_utils.py       # Text parsing logic to extract tasks
│   └── image_utils.py       # Image resizing, denoising, etc.
├── requirements.txt         # Python dependencies
└── README.md                # ← You’re here
```

- **`main.py`**  
  Parses command-line arguments, coordinates image preprocessing, OCR, and text parsing, and saves output files.

- **`ocr_utils.py`**  
  Contains helper functions for invoking Tesseract, handling PDF-to-image conversion, and basic text cleaning.

- **`parse_utils.py`**  
  Implements logic to parse raw OCR text and identify task-like lines (e.g., lines starting with “-”, “*”, or “TODO”).

- **`image_utils.py`**  
  Includes image preprocessing routines (grayscale, thresholding, noise removal, resizing).

- **`data/`**  
  Folder for test images. Feel free to add your own images to evaluate the workflow.

- **`outputs/`**  
  Where JSON and text outputs are stored by default. Create this folder if it doesn’t already exist.

---

## Configuration

- **OCR Engine**  
  By default, uses Tesseract. If you want to switch to a different OCR (e.g., Google Cloud Vision), modify `ocr_utils.py` accordingly.

- **Threshold and Preprocessing Parameters**  
  In `image_utils.py`, you can adjust:
  ```python
  THRESHOLD_BLOCK_SIZE = 11
  THRESHOLD_C = 2
  BLUR_KERNEL_SIZE = (5, 5)
  ```
  to fine-tune for different lighting conditions or handwriting styles.

- **Parsing Rules**  
  In `parse_utils.py`, update regular expressions (e.g., `r"^\s*[-*]|TODO"`) to match your specific to-do formats.

---

## Extending the Project

- **Language Support**  
  Integrate additional language models or keyword lists to support tasks in languages other than English.

- **GUI/Frontend**  
  Build a simple web interface (e.g., using Flask or Streamlit) to allow drag-and-drop of images and display tasks.

- **Mobile Integration**  
  Package as a mobile app using frameworks like Kivy or React Native for on-device OCR and task extraction.

- **Cloud Deployment**  
  Containerize the app with Docker and deploy to AWS, GCP, or Azure. Add a REST API endpoint for remote usage.

---

## Troubleshooting

- **Tesseract not found (`TesseractNotFoundError`)**  
  → Ensure Tesseract is installed and in your system PATH. On macOS, you might need to add `/usr/local/bin` to your PATH if installed via Homebrew.

- **OCR output is noisy or inaccurate**  
  → Try different preprocessing steps: adjust thresholding parameters or use Gaussian blur to improve OCR results.  

- **Unicode errors (`UnicodeDecodeError`)** when reading OCR output  
  → Ensure Tesseract is invoked with `--oem 3 --psm 6`, or explicitly specify UTF-8 output by appending `-c tessedit_create_hocr=0`.

- **No tasks detected**  
  → Check if the input image has clear, legible text. Also verify the parsing rules in `parse_utils.py` match your bullet/checkbox format.

---

## Contributing

1. **Fork** the repository and create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
2. **Implement** your changes and test thoroughly.  
3. **Commit** with descriptive messages:
   ```
   git commit -m "Add preprocessing for low-light images"
   ```
4. **Push** to your fork and open a Pull Request against `main`.  
5. We will review, provide feedback, and merge if everything looks good.

Please follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) and write clear docstrings.

---

## License

This project is licensed under the **MIT License**. See [LICENSE](../../LICENSE) for details.
