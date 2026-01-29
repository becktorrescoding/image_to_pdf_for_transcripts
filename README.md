# OCR Document Search Tool

A Python utility that searches through image files and PDFs using Optical Character Recognition (OCR) to find documents containing specific text patterns, particularly useful for locating patient records or documents by name.

## Features

- **OCR Text Search**: Searches through images and PDFs using Tesseract OCR
- **Multiple Format Support**: Handles PDF, JPG, JPEG, PNG, BMP, and TIFF files
- **Fuzzy Matching**: Falls back to partial name matching if exact match fails
- **Date Filtering**: Allows refinement of search results by admission date
- **PDF Generation**: Converts matched documents to searchable PDFs using OCRmyPDF
- **Recursive Search**: Searches through entire directory structures

## Prerequisites

### Required Software

1. **Python 3.7+**
2. **Tesseract OCR** - Install from [tesseract-ocr](https://github.com/tesseract-ocr/tesseract)
   - Windows: Download installer from GitHub releases
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

### Python Dependencies

Install required packages:

```bash
pip install ocrmypdf pytesseract pillow
```

## Installation

1. Clone or download this repository
2. Install Tesseract OCR for your operating system
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure the script (see Configuration section)

## Configuration

Before running the script, you need to set two important paths:

### 1. Output PDF Path
Edit line 8 in `Main.py`:
```python
output_pdf = Path("path/to/output/document.pdf")
```
Replace with your desired output location for processed PDFs.

### 2. Input Folder Path
Edit line 96 in `Main.py`:
```python
input_tiff = Path("path/to/input/folder")
```
Replace with the folder containing your documents to search.

**Note**: For network drives, use forward slashes in the path (e.g., `//server/share/folder`).

## Usage

Run the script from the command line:

```bash
python Main.py
```

### Search Process

1. **Enter Name**: When prompted, enter the first and last name to search for
   ```
   Enter first and last name: John Smith
   ```

2. **Exact Match**: The script searches all images for an exact match
   - If one match is found, it's automatically converted to PDF
   - If multiple matches are found, you'll be prompted for an admission date

3. **Date Filtering**: If multiple matches exist, enter the admission date
   ```
   Enter Date of Admission: 01/15/2024
   ```

4. **Fallback Search**: If no exact match is found, the script attempts partial matching
   - Matches documents containing at least 50% of the search keywords

## How It Works

### Main Functions

- **`search_folders(folder_path, search_for)`**: Primary search function that recursively scans directories
- **`search_fallback(folder_path, search_for)`**: Partial keyword matching when exact search fails
- **`search_images(matched_files, search_for)`**: Filters results by additional criteria (e.g., date)
- **`convert_tiff(tiff)`**: Converts matched document to searchable PDF using OCRmyPDF

### Supported File Types

- PDF (`.pdf`)
- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- BMP (`.bmp`)
- TIFF (`.tif`, `.tiff`, `.TIF`)

## Output

- Successfully matched documents are converted to searchable PDFs
- Output location is specified in the `output_pdf` variable
- OCRmyPDF applies deskewing and forced OCR to improve readability

## Error Handling

The script includes error handling for:
- File reading errors
- OCR processing failures
- Invalid image formats

Errors are logged to the console with the affected file path.

## Limitations

- OCR accuracy depends on image quality and text clarity
- Processing large directories can be time-consuming
- Network drive access may be slower than local storage
- Partial matching threshold is fixed at 50% of keywords

## Troubleshooting

### "Tesseract not found" Error
- Ensure Tesseract is installed and added to your system PATH
- On Windows, you may need to set the path manually:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```

### OCRmyPDF Errors
- Ensure Ghostscript is installed (required by OCRmyPDF)
- Check that output directory exists and is writable

### No Matches Found
- Verify image quality is sufficient for OCR
- Try partial name search (first or last name only)
- Check for spelling variations in documents

## Future Enhancements

Potential improvements noted in the code:
- Configurable output and input paths via command-line arguments
- Configuration file support
- Adjustable partial match threshold
- Batch processing mode
- GUI interface

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Tomás Beck Torres

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/becktorrescoding/image_to_pdf_for_transcripts/issues) if you want to contribute.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact

becktorrescoding@gmail.com
