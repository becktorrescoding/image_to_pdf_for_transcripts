# Image to PDF Converter & OCR Search Tool

A Python utility that combines OCR-based document search with image-to-PDF conversion capabilities. Search through image files and PDFs using Optical Character Recognition (OCR) to find documents containing specific text patterns, or bulk convert images to searchable PDFs. Particularly useful for locating and processing patient records or documents by name.

## Features

- **Dual Mode Operation**: Choose between document search mode or bulk conversion mode
- **OCR Text Search**: Searches through images and PDFs using Tesseract OCR
- **Multiple Format Support**: Handles PDF, JPG, JPEG, PNG, BMP, and TIFF files
- **Fuzzy Matching**: Falls back to partial name matching (50% threshold) if exact match fails
- **Date Filtering**: Refine search results by admission year when multiple matches exist
- **Interactive Viewing**: Preview matched documents before converting
- **PDF Generation**: Converts matched documents to searchable PDFs using OCRmyPDF
- **Bulk Conversion**: Convert entire folders of images to PDFs in one operation
- **Recursive Search**: Searches through entire directory structures
- **User-Friendly Prompts**: Interactive command-line interface with clear options

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

Before running the script, you **must** configure the input and output paths:

### Input and Output Paths
Edit lines 12-13 in `image_to_pdf.py`:
```python
output_path = Path(r"C:/path/to/output/folder")
input_path = Path(r"C:/path/to/input/folder")
```

**Important Notes:**
- Both paths are required - the script will raise an error if either is empty
- Use the `r` prefix before the string to handle Windows paths correctly
- For network drives, use forward slashes (e.g., `r"//server/share/folder"`)
- The output_path should be a folder, not a specific filename
- The input_path should point to the root folder containing your documents

## Usage

Run the script from the command line:

```bash
python image_to_pdf.py
```

### Mode Selection

The script first asks which mode you want to use:

```
Would you like to find or bulk convert files? (f/c):
```

- **`f`** - Search mode: Find specific documents by name
- **`c`** - Bulk convert mode: Convert all images in input folder to PDFs

---

### Search Mode (f)

#### 1. Enter Name
When prompted, enter the first and last name to search for:
```
Enter first and last name: John Smith
```

#### 2. Search Results

**Single Match Found:**
```
File found.
Would you like to view the image, convert it to PDF, or quit? (V/C/Q):
```
- **`V`** - View the image in your default image viewer
- **`C`** - Convert the image to a searchable PDF
- **`Q`** - Quit without taking action

**Multiple Matches Found:**
If multiple documents match, you'll be prompted for the admission year:
```
More than one matching documents found.
Enter Year of Admission (YY): 24
```
The script then filters by the year and presents options to view, convert, or quit.

**No Exact Match:**
If no exact match is found, the script automatically attempts partial matching (50% of keywords). If partial matches are found, you'll see the same interactive options.

**Too Many Matches:**
If multiple documents still match after date filtering, the script creates a text file listing all matched files:
```
matched files.txt
```

---

### Bulk Convert Mode (c)

Converts all images in the input folder and subfolders to searchable PDFs:
```
Would you like to find or bulk convert files? (f/c): c
```

The script will:
1. Recursively scan the input folder
2. Process all supported image formats
3. Save converted PDFs to the output folder
4. Display progress and any errors encountered

## How It Works

### Main Functions

- **`search_folders(folder_path, search_for)`**: Primary search function that recursively scans directories for exact text matches
- **`search_fallback(folder_path, search_for)`**: Partial keyword matching (50% threshold) when exact search fails
- **`search_images(matched_files, date)`**: Filters results by admission year and handles multiple matches
- **`convert_image(image)`**: Converts a single matched document to searchable PDF using OCRmyPDF with deskewing
- **`bulk_convert(input_folder, output)`**: Batch processes all images in a folder to PDFs

### Workflow

1. **Initialization**: Validates that input and output paths are configured
2. **Mode Selection**: User chooses between search or bulk convert
3. **Search Mode**:
   - Recursively scans folders
   - Performs OCR on each image
   - Matches against search criteria
   - Provides interactive options for viewing/converting
4. **Bulk Mode**:
   - Walks through all subdirectories
   - Converts all supported image formats to PDF
   - Saves to output location

### Supported File Types

- PDF (`.pdf`)
- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- BMP (`.bmp`)
- TIFF (`.tif`, `.tiff`, `.TIF`)

## Output

### Search Mode
- **Interactive Preview**: View matched documents before converting
- **Searchable PDFs**: Converted documents saved to configured output path
- **Match List**: When multiple matches exist after filtering, creates `matched files.txt` with all file paths
- **OCR Enhancement**: OCRmyPDF applies deskewing and forced OCR for improved readability

### Bulk Convert Mode
- All images in input folder converted to PDFs
- Maintains folder structure in output location
- Progress displayed in console

## Error Handling

The script includes comprehensive error handling for:
- **Configuration Validation**: Ensures input and output paths are set before execution
- **File Reading Errors**: Catches and reports issues opening image files
- **OCR Processing Failures**: Handles Tesseract errors gracefully
- **Invalid Image Formats**: Skips unsupported files with error messages
- **Missing Directories**: Validates input folder exists before processing
- **User Input Validation**: Handles invalid menu choices with retry prompts

All errors are logged to the console with the affected file path and error description.

## Limitations

- OCR accuracy depends on image quality and text clarity
- Processing large directories can be time-consuming
- Network drive access may be slower than local storage
- Partial matching threshold is fixed at 50% of keywords
- Bulk conversion processes all files sequentially (no parallel processing)
- Year-based filtering expects two-digit year format (YY)
- Generated `matched files.txt` overwrites previous results

## Troubleshooting

### "Please provide input and output path" Error
- Ensure both `input_path` and `output_path` variables are configured in the script
- Check that the paths are not empty strings (`r""`)

### "Tesseract not found" Error
- Ensure Tesseract is installed and added to your system PATH
- On Windows, you may need to set the path manually:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```

### OCRmyPDF Errors
- Ensure Ghostscript is installed (required by OCRmyPDF)
- Check that output directory exists and is writable
- Verify sufficient disk space for PDF generation

### No Matches Found
- Verify image quality is sufficient for OCR
- Try partial name search (first or last name only)
- Check for spelling variations in documents
- Ensure documents contain searchable text (not handwritten)

### Image Won't Open for Viewing
- Ensure you have a default image viewer configured
- Check file permissions
- Verify the image file isn't corrupted

### Bulk Conversion Issues
- Ensure input folder path is correct and accessible
- Check that you have write permissions to the output folder
- Verify images are in supported formats

## Future Enhancements

Potential improvements for future versions:
- Command-line arguments for paths instead of hardcoded variables
- Configuration file support (YAML/JSON)
- Parallel processing for bulk conversions
- Progress bar for large batch operations
- Adjustable partial match threshold via user input
- GUI interface for non-technical users
- Export search results to CSV/Excel
- Advanced filtering options (date ranges, file types)
- Logging to file for audit trail
- Resume capability for interrupted bulk conversions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright © 2025 Tomas Beck Torres

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact

Tomás Beck Torres - becktorrescoding@gmail.com | bectorrescoding.odoo.com

Project Link: [https://https://github.com/becktorrescoding/image_to_pdf_for_transcripts](https://https://github.com/becktorrescoding/image_to_pdf_for_transcripts)
