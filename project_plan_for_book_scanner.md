# Project Plan: Book to Markdown Scanner

## Overview
This project converts scanned book page images into Markdown files using OCR. Scanning is performed externally with vFlat Scan (or another scanner) which exports the book pages as images. The Python program in this repo will take those images, run OCR, and produce Markdown files where each page begins with a page tag for later referencing.

## Part 1 — Scanning (vFlat Scan)
- Use vFlat Scan to capture the physical book pages.
- Export pages as individual image files (one file per page), named in a consistent sequence (e.g., `page_001.jpg`, `page_002.jpg`).
- Store exported images in a folder `images_that_should_be_impored` inside the Book folder.
- Recommended export settings: high resolution (300–600 DPI), lossless or high-quality JPEG/PNG, consistent orientation.

## Part 2 — This Project (Python OCR → Markdown)
### Goals
- Convert a folder of page images into Markdown files.
- Each page's markdown begins with a page tag: `#{page X}` (X is the page number).
- Produce individual Markdown files in `exported_markdown_files` and maintain a mapping file `image_to_markdown_page_map.md` that maps image names to the generated Markdown filenames and page numbers.

### CLI & Usage
- Script entrypoint: `convert_images_to_md.py` (or similar).
- Command-line arguments:
  - `--input` / `-i`: input folder containing images (required).
  - `--output` / `-o`: output folder for generated markdown files (required).
  - `--map-file` / `-m`: path to `image_to_markdown_page_map.md` (defaults to output folder root).
  - `--ocr-engine`: choose OCR backend (e.g., `tesseract`, `easyocr`) (optional).
  - `--preprocess`: enable/disable image preprocessing steps (optional).
  - `--verbose` / `-v`: logging verbosity.

Example:
```
python convert_images_to_md.py --input ./images_that_should_be_impored --output ./exported_markdown_files --map-file ./image_to_markdown_page_map.md
```

### Processing rules
- Process images in alphanumeric order.
- For each image:
  1. Optionally preprocess (deskew, denoise, binarize, crop borders).
  2. Run OCR to get text.
  3. Create a Markdown file named using a predictable pattern (e.g., `page_001.md` or derived from original image name).
  4. Insert the page tag as the first line: `#{page X}` (where X is the page number determined from filename or sequence index).
  5. Append recognized text beneath the page tag using paragraph breaks for blank lines found in OCR output.
  6. Save the Markdown file to `exported_markdown_files`.
  7. Update or append a row to `image_to_markdown_page_map.md` mapping image filename → markdown filename → page number → timestamp.

### `image_to_markdown_page_map.md` format
Use a simple Markdown table with headers, for example:

| image_name | markdown_file | page_number | converted_at |
|---|---:|---:|---|
| page_001.jpg | page_001.md | 1 | 2026-08-22T12:00:00Z |

The script must create the map file if missing and append new rows for subsequent runs. If an image is reprocessed, the script can either update the existing row or append a new row and log the re-run (configurable behavior).

### OCR engine & dependencies
- Minimal recommended stack:
  - Python 3.10+
  - `pytesseract` + Tesseract OCR (external binary) *or* `easyocr` for a Python-only option.
  - `Pillow` for image I/O.
  - `opencv-python` for preprocessing (optional but recommended).
  - `python-dotenv` (optional) for configuration.
- If using Tesseract, document how to install Tesseract on Windows (link in README).

### Image preprocessing suggestions
- Convert to grayscale and apply adaptive thresholding for poor contrast.
- Remove borders and deskew pages if necessary (OpenCV Hough / contour methods or use `deskew`).
- Resize small images to improve OCR accuracy.
- If book pages contain multi-column layouts, consider a layout analysis step (advanced).

### Markdown conversion rules / heuristics
- Keep paragraph breaks from OCR as blank lines in Markdown.
- Use basic punctuation heuristics to avoid merging sentences incorrectly.
- Do not attempt to infer chapters or headings automatically initially; keep raw OCR text, optionally exposing a `--postprocess` flag to run heuristics.
- Preserve simple inline formatting only if the OCR engine supports it (advanced).

### File & Folder Structure
Book folder (single example):

BookName/
- images_that_should_be_impored/    ← input images from vFlat Scan
- exported_markdown_files/          ← output Markdown pages
- image_to_markdown_page_map.md     ← mapping file created/updated by the script

Notes:
- The script should create `exported_markdown_files` and the map file if they do not exist.
- Use safe filename generation for Markdown files to avoid collisions.

### Error handling & logging
- Produce a concise log per run listing processed images, skipped images, and failures.
- On OCR errors, write a debug copy of the preprocessed image into a `failed/` subfolder for inspection.
- Return non-zero exit code on fatal errors (like missing input folder).

### Testing & Sample Data
- Include a `samples/` folder with a few representative scanned pages (one-column, headers/footers, and a two-column page if possible).
- Add unit tests for filename parsing, map file appending, and simple OCR/text-processing utilities (mock OCR responses for tests where actual OCR is not desired).

### Roadmap & Milestones
1. Create planning doc (this file).  ← current
2. Scaffold repo and CLI parser.
3. Implement basic OCR pipeline with Tesseract and minimal preprocessing.
4. Implement mapping file creation and append behavior.
5. Add README, sample images, and tests.
6. Improve preprocessing and add optional layout detection.

### Open Questions / Decisions
- Which OCR backend do you prefer (Tesseract vs EasyOCR)?
- Do you want the script to attempt automatic chapter/heading detection later?
- How should re-processing of the same image be handled in the map file (overwrite vs append)?

---

If you'd like, I can now scaffold the project (create the folders and a starter `convert_images_to_md.py`), or implement the full OCR script using Tesseract. Which would you prefer as the next step?

## Part 3 — Proofreading with Copilot

### Goals
- Ensure converted pages are human-validated by Copilot before marking them as final.
- Add a two-stage tag workflow: initial `#{to_be_proof_read}` and final `#{validated_by_copilot}`.

### Workflow
- The converter script inserts `#{to_be_proof_read}` as the first tag line of every generated Markdown page.
- A separate validation step (manual review assisted by Copilot) will open each page marked `#{to_be_proof_read}` and allow a reviewer to correct OCR errors.
- After Copilot or the reviewer confirms correctness, the script or tool will replace the tag with `#{validated_by_copilot}`.

### Implementation notes
- Add a CLI flag `--mark-to-review` (default behavior) to insert `#{to_be_proof_read}` on creation.
- Add a CLI subcommand `validate` or `--validate` which:
  - Scans the output folder for pages with `#{to_be_proof_read}`.
  - Optionally runs Copilot-assisted proofreading (this can be a manual step where Copilot provides suggestions).
  - Rewrites the first tag to `#{validated_by_copilot}` after confirmation and updates the map file with validation timestamp and reviewer (e.g., `copilot`).
- In the `image_to_markdown_page_map.md` table, add `validated_at` and `validated_by` columns to track validation state.

### Safety & audit
- Keep previous versions or record validation events (timestamp + reviewer) rather than destructive overwrites, to allow audit and rollback.
- For re-runs, preserve existing `validated_by` entries unless revalidated explicitly.

### Open questions
- Do you want Copilot to auto-apply suggested fixes, or should a human approve each change before the tag is flipped?
