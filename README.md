A small linux app for training note recognition.

## Run from source
### Requirements

- Python 3
- Packages:
  - pymupdf
  - pillow

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the app
```bash
python main.py

## Build Executable
Package the app into an executable so it can run without Python.

### Install PyInstaller
```bash
pip install pyinstaller```

### Build
#### Linux/macOS
```bash
pyinstaller --onedir \ --name sight-reading-trainer \ --add-data "pdfs:pdfs" \ --hidden-import=PIL.ImageTk \ --hidden-import=PIL._tkinter_finder \ --hidden-import=PIL._imagingtk \ main.py
```
The packaged app will be in 
```
dist/sight-reading-trainer/
```
