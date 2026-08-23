# Book to Markdown Scanner

Starter repository for converting scanned book pages (images) into Markdown using OCR.

## What I added
- `convert_images_to_md.py`: starter CLI that creates markdown files with `#{to_be_proof_read}` tags and a mapping table.
- `requirements.txt`: suggested Python packages.
- `setup_venv.ps1` / `setup_venv.sh`: helper scripts to create a virtual environment.
- `.gitignore`: Python-focused ignore rules and excludes image folders by default.
- Project folders: `images_that_should_be_impored`, `exported_markdown_files`, `samples`.
- `diagrams/process_flow.md` and `project_plan_for_book_scanner.md` (planning files).

## Quick start (Windows PowerShell)
```powershell
cd C:\Users\JuliusJe\Documents\VsCode\book_to_markdown_scanner
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Quick start (Unix)
```bash
cd /path/to/book_to_markdown_scanner
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## WSL / Bash on Windows
If you use Windows Subsystem for Linux (WSL) you can run the project in a Linux environment:

```bash
# open WSL shell and change to the project folder (Windows path mounted under /mnt)
cd /mnt/c/Users/JuliusJe/Documents/VsCode/book_to_markdown_scanner

# create and activate virtualenv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# install Tesseract inside WSL (if you will use pytesseract)
sudo apt update
sudo apt install -y tesseract-ocr

# run the starter converter
python convert_images_to_md.py -i images_that_should_be_impored -o exported_markdown_files
```

Notes:
- Files created under `/mnt/c/...` are immediately accessible from Windows Explorer and VS Code.
- To open the project in the WSL-aware VS Code session, run `code .` from the WSL shell (requires VS Code and the Remote - WSL extension).
- Use the `setup_venv.sh` script as a convenience inside WSL if preferred.

## Running Git GUI

If you prefer a graphical Git client, this project includes small helper scripts to launch `git gui`:

- Windows PowerShell helper: `run_git_gui.ps1`
	- Usage (PowerShell):
		```powershell
		# launch git-gui for the current folder
		.\run_git_gui.ps1

		# or specify a repo path
		.\run_git_gui.ps1 -RepoPath C:\Users\JuliusJe\Documents\VsCode\book_to_markdown_scanner
		```
	- The script first tries `git gui` on PATH, then falls back to common Git for Windows locations.

- WSL / Bash helper: `run_git_gui_wsl.sh`
	- Usage (WSL):
		```bash
		./run_git_gui_wsl.sh /mnt/c/Users/JuliusJe/Documents/VsCode/book_to_markdown_scanner
		```
	- Notes: inside WSL this will try `git gui` (requires an X server / DISPLAY) or attempt to call the Git for Windows `git-gui.exe` via the mounted Windows path.

If you don't have `git gui` installed:
- On Windows: install Git for Windows (https://git-scm.com/download/win) — it includes `git-gui`.
- On WSL: install `tcl/tk` and `git-gui` (if your distro provides it) and run an X server on Windows (e.g., VcXsrv or X410), or use the Windows `git-gui.exe` fallback above.

## Running the starter converter
```bash
python convert_images_to_md.py -i images_that_should_be_impored -o exported_markdown_files
```

Notes:
- This starter does not run OCR yet. Install Tesseract separately (https://github.com/tesseract-ocr/tesseract) for `pytesseract` to work.
- Consider using Git LFS for large image files: https://git-lfs.github.com/
- Next steps: implement preprocessing (deskew/denoise), OCR, and the proofreading validation flow.

## Recommended project files to add later
- `LICENSE` (e.g., MIT)
- `CONTRIBUTING.md`
- `tests/` with unit tests
- `pyproject.toml` or `setup.cfg` if packaging
- GitHub Actions workflow for tests
