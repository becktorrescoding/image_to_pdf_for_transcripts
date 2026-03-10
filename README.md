# Image to PDF Converter & OCR Search Tool

A Python GUI application that combines OCR-based document search with image-to-PDF conversion capabilities. Built to help universities digitise and manage pre-digital era scanned transcripts and degrees. Features an intuitive graphical interface with two operation modes: search through image files and PDFs using Optical Character Recognition (OCR) to find specific documents, or bulk convert entire folders of images to searchable PDFs — all without needing to edit code.

## Features

- **Graphical User Interface**: Easy-to-use GUI built with tkinter - no code editing required
- **Dual Operation Modes**: Choose between Search Mode and Bulk Convert Mode via radio buttons
- **Folder Browser**: Browse and select input/output folders with native file dialogs
- **OCR Text Search**: Searches through images and PDFs using Tesseract OCR
- **Bulk Conversion**: Convert all images in a directory (and subdirectories) to searchable PDFs
- **Multiple Format Support**: Handles PDF, JPG, JPEG, PNG, BMP, and TIFF files
- **Fuzzy Matching**: Falls back to partial name matching (50% threshold) if exact match fails
- **Year Filtering**: Optional field to refine search results by year
- **Real-time Logging**: Processing status displayed in scrollable log window with progress counters
- **Smart Filename Generation**: Automatically names output PDFs using information extracted from the document (name, degree/admission date, document type)
- **Threaded Processing**: Non-blocking operations keep GUI responsive during long tasks
- **Recursive Search**: Searches through entire directory structures
- **User-Friendly**: Clear error messages, success notifications, and conversion summaries

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

1. **Clone or download this repository**

2. **Install Tesseract OCR** - Download from [tesseract-ocr](https://github.com/tesseract-ocr/tesseract)
   - Windows: Download installer from GitHub releases
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

3. **Install Python dependencies:**
   ```bash
   pip install ocrmypdf pytesseract pillow
   ```

4. **Launch the GUI:**
   ```bash
   python image_to_pdf.py
   ```

## Screenshots

### Main Interface
The application features a clean, intuitive interface:
- **Folder Selection**: Browse buttons for easy path selection
- **Mode Selection**: Radio buttons to switch between Search and Bulk Convert modes
- **Search Fields**: Name and optional year input (Search Mode only)
- **Processing Log**: Real-time status updates in scrollable text area
- **Green Start Button**: Initiates processing

### Typical Workflows

**Search Mode:**
1. Select input folder containing scanned images
2. Select output folder for converted PDFs
3. Select "Search Mode"
4. Enter student name
5. (Optional) Enter graduation year for filtering
6. Click "Start Search"
7. Monitor progress in log window
8. Receive success notification when complete

**Bulk Convert Mode:**
1. Select input folder containing images
2. Select output folder for converted PDFs
3. Select "Bulk Convert Mode"
4. Click "Start Search"
5. Monitor progress in log window (shows X/total count)
6. Receive summary dialog when complete

## Configuration

**No configuration needed!** The GUI allows you to select folders through browse dialogs at runtime. Simply:

1. Launch the application
2. Click "Browse" to select your input folder (where images are located)
3. Click "Browse" to select your output folder (where PDFs will be saved)
4. Choose your operation mode and click "Start Search"

**Optional**: If you want to set default paths in the code, edit `image_to_pdf.py`:
- Modify `self.input_path` and `self.output_path` initialization in `__init__()`

## Usage

### Running the Application

```bash
python image_to_pdf.py
```

A graphical window will open with the following interface:

---

### Step-by-Step Usage

#### 1. Select Folders
- **Input Folder**: Click "Browse" next to "Input Folder" and select the folder containing your images
- **Output Folder**: Click "Browse" next to "Output Folder" and select where you want PDFs saved

#### 2. Choose Operation Mode
Use the radio buttons to select your mode:
- **Search Mode**: Find specific documents by name (shows search fields)
- **Bulk Convert Mode**: Convert all images in the input folder (hides search fields)

#### 3. Search Mode — Enter Search Criteria
- **Search Name**: Type the student name to search for (e.g., "John Smith")
- **Year (Optional)**: Enter a graduation year (e.g., "98") to filter results. Leave blank to skip year filtering.

#### 4. Start Processing
Click the green **"Start Search"** button to begin.

#### 5. Monitor Progress
The Processing Log window shows real-time status.

**Search Mode example:**
```
=== Starting Search Mode ===
Searching for John Smith
Match found: scan_001.jpg
No exact matches found. Trying partial match...
Partial match found: scan_002.jpg
Filtering by year: 98
Found 1 matching file(s).
Converting scan_002.jpg to PDF...
✓ Successfully converted to: scan_002.pdf
Search and conversion complete!
```

**Bulk Convert Mode example:**
```
=== Starting Bulk Convert Mode ===
Found 42 image(s) to convert.

Converting: scan_001.jpg
  📄 Generated filename: Smith_John_A_Bachelor_of_Commerce_June_12_1979.pdf
  ✓ Success (1/42)

Converting: scan_002.png
  📄 Generated filename: Doe_Jane_Transcript_March_3_1975.pdf
  ✓ Success (2/42)

Converting: scan_003.jpg
  ⚠ Could not detect document type — using original filename.
  ✓ Success (3/42)
...
==================================================
Bulk conversion complete!
Successfully converted: 42/42
Errors: 0
==================================================
```

#### 6. Results
- **Search Mode**: Success message box appears; PDF saved to output folder
- **Bulk Convert Mode**: Summary dialog shows total converted and any errors
- If no matches found (Search Mode), you'll see an informational message

---

### Search Behavior

**Exact Match First:**
The application searches for the exact name you entered in image text (via OCR).

**Automatic Fallback:**
If no exact match is found, it automatically tries partial matching:
- Splits your search into keywords (e.g., "John Smith" → ["John", "Smith"])
- Finds documents containing at least 50% of the keywords
- Example: A document with only "John" would match

**Year Filtering:**
If you enter a year, matched files are filtered to only those containing that year in their text.

---

### Example Workflows

**Scenario 1**: Find and convert a transcript for "Jane Doe" who graduated in 1998

1. Launch app: `python image_to_pdf.py`
2. Browse input to: `C:/University/ScannedRecords`
3. Browse output to: `C:/University/Converted`
4. Select **Search Mode**
5. Enter name: `Jane Doe`
6. Enter year: `98`
7. Click "Start Search"
8. Find PDF at: `C:/University/Converted/scan_xyz.pdf`

**Scenario 2**: Bulk convert an entire archive of scanned degrees

1. Launch app: `python image_to_pdf.py`
2. Browse input to: `C:/University/DegreeArchive`
3. Browse output to: `C:/University/Converted`
4. Select **Bulk Convert Mode**
5. Click "Start Search"
6. Wait for completion summary

## How It Works

### GUI Architecture

The application uses a **class-based tkinter GUI** with the following structure:

```
ImageToPDFApp (Main Class)
├── __init__()              # Initialize window and variables
├── create_widgets()        # Build GUI interface
├── toggle_mode()           # Show/hide search fields based on mode
├── browse_input()          # Handle input folder selection
├── browse_output()         # Handle output folder selection
├── start_search()          # Validate inputs and start thread
├── do_search()             # Route to correct mode (runs in thread)
├── search_mode()           # Search Mode workflow
├── bulk_convert_mode()     # Bulk Convert Mode workflow
├── search_folders()        # Exact text match via OCR
├── search_fallback()       # Partial keyword matching
├── search_images()         # Filter by year
├── generate_filename()     # Extract fields from OCR text and build filename
├── convert_image()         # Convert single image to searchable PDF
└── log()                   # Display messages in GUI
```

### Automatic Filename Generation (Search Mode)

When a document is converted in Search Mode, the output PDF is automatically named using information extracted from the OCR text rather than the original scanned filename.

**Degree format:**
```
LastName_FirstName_MI_DegreeName_Month_Day_Year.pdf
```
Example: `Smith_John_A_Bachelor_of_Commerce_June_12_1979.pdf`

**Transcript format:**
```
LastName_FirstName_MI_Transcript_Month_Day_Year.pdf
```
Example: `Smith_John_A_Transcript_March_3_1975.pdf`

**How it works:**
1. Detects document type by looking for `"Degree Received"` or `"Date of Admission"` in the OCR text
2. Extracts the student name — handles both `Last, First MI` and `First MI Last` formats
3. For degrees: extracts the degree name from the text following `"Degree Received"` and the graduation date to its right
4. For transcripts: extracts the admission date from the text following `"Date of Admission"`
5. Normalises dates to a consistent `Month_DD_YYYY` format regardless of how they appear in the document — both `June 12, 1979` and `06/12/79` will produce `June_12_1979`. 2-digit years are expanded automatically (`79` → `1979`, years `00–19` are assumed to be 2000s)
6. Assembles the parts into a clean filename, stripping invalid characters

**Fallback behaviour:**
If any field cannot be extracted, a warning is logged and the original scanned filename is used instead. This ensures conversion always completes even if the OCR output is unclear.

### Search Mode Workflow

1. **User Input**: User enters name and optional year via GUI fields
2. **Validation**: System checks all required fields are filled
3. **Threading**: Search runs in background thread (GUI stays responsive)
4. **OCR Processing**: Each image is processed with Tesseract OCR
5. **Text Matching**: Extracted text is compared against search criteria
6. **Fallback**: If no exact match, automatically tries partial matching
7. **Filtering**: Optional year filter applied if provided
8. **Conversion**: First matched file converted to PDF with OCRmyPDF
9. **Notification**: User notified of success/failure

### Bulk Convert Mode Workflow

1. **Validation**: System checks input and output folders are provided
2. **File Discovery**: Recursively counts all valid image files in input folder
3. **Threading**: Conversion runs in background thread (GUI stays responsive)
4. **Batch Conversion**: Each image converted to searchable PDF with OCRmyPDF
5. **Progress Tracking**: Log shows per-file results and running count (X/total)
6. **Error Handling**: Individual file errors are logged; processing continues
7. **Summary**: Completion dialog reports total converted and error count

### Technical Details

- **OCR Engine**: Tesseract (via pytesseract) extracts text from images
- **PDF Creation**: OCRmyPDF creates searchable PDFs with deskewing and forced OCR
- **Threading**: `threading.Thread` prevents GUI freezing during processing
- **File Handling**: `pathlib.Path` for cross-platform path management
- **Error Handling**: Try-except blocks catch and log errors gracefully

### Supported File Types

- PDF (`.pdf`)
- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- BMP (`.bmp`)
- TIFF (`.tif`, `.tiff`, `.TIF`)

## Output

### Search Mode — Success
- **Searchable PDF**: First matched document saved to output folder with original filename + `.pdf`
- **Log Messages**: Real-time progress shown in GUI log window
- **Success Dialog**: Pop-up notification confirms completion

### Bulk Convert Mode — Success
- **Searchable PDFs**: All converted documents saved to output folder with auto-generated structured filenames (falls back to original filename if document type cannot be detected)
- **Progress Log**: Per-file status showing generated filename and running count (e.g., `✓ Success (12/42)`)
- **Summary Dialog**: Reports total files converted and number of errors

### No Matches Case (Search Mode)
- **Informational Dialog**: "No matching files found" message
- **Log Details**: Shows search attempts and why no matches were found

### Error Case
- **Error Dialog**: Specific error message displayed
- **Log Details**: Full error details in log window for debugging
- **Bulk Convert**: Errors are logged per file; remaining files continue processing

## Error Handling

The GUI includes comprehensive error handling:

### Input Validation
- **Empty Fields**: Error dialog if name or paths missing
- **Invalid Paths**: System validates folder existence before processing
- **Mode-aware**: Search Mode requires a name; Bulk Convert Mode does not

### Processing Errors
- **OCR Failures**: Logged with filename and error details
- **Image Read Errors**: Skips corrupted files, continues processing others
- **Conversion Errors**: Detailed error message logged per file

### User Experience
- **Non-blocking Errors**: GUI remains responsive even during errors
- **Error Logs**: All errors displayed in log window for review
- **Graceful Degradation**: Partial matches attempted if exact match fails (Search Mode)

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Please select both input and output folders." | Missing folder paths | Browse and select both folders |
| "Please enter a name to search for." | Search Mode with empty name field | Enter a name to search |
| "Error processing [file]" | Corrupted or unreadable image | Check image file integrity |
| "No matching files found" | No documents contain search text | Verify spelling, try partial name |
| Tesseract error | OCR engine not installed | Install Tesseract OCR |

## Privacy & Data Security

All processing is performed **entirely locally on your machine**. No files, text, or metadata are transmitted over the internet at any point.

| Dependency | Data Collection | Network Access |
|------------|----------------|----------------|
| Tesseract OCR | None | None — fully offline |
| OCRmyPDF | None | None — fully offline |
| Pillow | None | None — fully offline |
| tkinter | None | None — fully offline |

This makes the tool suitable for handling sensitive documents such as university transcripts and degrees, where student records should remain confidential and within your institution's systems.

> **Tip**: For added assurance, you can run the application on an air-gapped machine or monitor outbound network traffic with a tool like Wireshark to independently verify no data leaves your system.

## Limitations

- **OCR Accuracy**: Depends on image quality, text clarity, and scan resolution
- **Processing Speed**: Large directories or high-resolution images can be slow
- **Network Drives**: May be slower than local storage; consider copying files locally first
- **Partial Match Threshold**: Fixed at 50% of keywords (not user-configurable in GUI)
- **Search Mode converts first match only**: Only the first matched file is converted; subsequent matches are ignored
- **Filename generation accuracy**: Auto-naming relies on OCR quality — poor scans may fall back to the original filename
- **Year Format**: Searches for year as a text string in OCR output; works with both 2-digit and 4-digit years depending on what appears in the document
- **GUI Responsiveness**: During OCR processing, only log updates; button disabled until complete
- **Memory Usage**: Processing very large images may consume significant RAM
- **Bulk Output Folder**: All converted files written to a flat output folder (subdirectory structure not preserved)

## Troubleshooting

### GUI Won't Open
**Symptom**: Double-clicking does nothing or window appears then closes
**Solutions**:
- Run from terminal to see error messages: `python image_to_pdf.py`
- Check Python version (requires 3.7+)
- Verify tkinter is installed: `python -m tkinter` (should open test window)

### "Tesseract not found" Error
**Symptom**: Error dialog when clicking "Start Search"
**Solutions**:
- Ensure Tesseract OCR is installed
- Add Tesseract to system PATH
- **Windows**: Manually set path in code:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```

### OCRmyPDF Errors
**Symptom**: PDF conversion fails
**Solutions**:
- Install Ghostscript (required by OCRmyPDF)
- Check output folder is writable
- Verify sufficient disk space
- Try with smaller/simpler image first

### No Matches Found (Search Mode)
**Symptom**: "No matching files found" message
**Solutions**:
- Verify image quality is clear enough for OCR
- Check spelling of search name
- Try searching for just first or last name
- Test with known document to verify OCR is working
- Images with handwriting may not work well

### GUI Freezes
**Symptom**: Window becomes unresponsive
**Solutions**:
- Wait - processing may take time for large folders
- Check log window for progress updates
- Force quit and try with smaller folder first
- Reduce image resolution if files are very large

### Browse Button Not Working
**Symptom**: Clicking Browse does nothing
**Solutions**:
- Check file system permissions
- Try running as administrator (Windows)
- Verify folder paths don't contain special characters

### Output PDF is Empty or Corrupted
**Symptom**: PDF created but contains no content
**Solutions**:
- Check original image contains readable text
- Verify image file isn't corrupted
- Try with different image format
- Increase image contrast before processing

## Future Enhancements

Potential improvements for future versions:

### GUI Improvements
- **Save/Load Settings**: Remember last used folders and mode
- **Theme Selection**: Light/dark mode options
- **Progress Bar**: Visual progress indicator during bulk conversion
- **Drag & Drop**: Drop files directly into window
- **Multi-file Conversion**: Convert all matched files in Search Mode (not just the first)
- **Preview Pane**: Show thumbnail of found images before converting

### Functionality
- **Advanced Search**: Search by multiple criteria (name AND date range)
- **Custom Match Threshold**: Slider to adjust partial match percentage
- **Export Results**: Save list of matched/converted files to CSV/Excel
- **Batch Processing**: Queue multiple searches to run sequentially
- **Preserve Subdirectory Structure**: Mirror input folder structure in bulk output
- **Bulk Output Naming**: Custom naming conventions for bulk converted files

### Performance
- **Parallel Processing**: Multi-threaded conversion for multiple files in bulk mode
- **Image Caching**: Cache OCR results to speed up repeated searches
- **Smart Scanning**: Skip previously converted files
- **Low-res Preview**: Quick preview mode before full OCR

### Advanced Features
- **Regular Expression Search**: Pattern matching for complex queries
- **File Management**: Option to move/copy originals after conversion
- **PDF Merging**: Combine multiple matched documents into single PDF
- **Annotation**: Add notes or highlights to converted PDFs
- **Cloud Integration**: Upload to Google Drive/Dropbox after conversion
- **Logging System**: Export detailed logs to file for auditing

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Tomás beck Torres

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

**How to contribute:**

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

**Areas where contributions are especially welcome:**
- GUI improvements (themes, layouts, new widgets)
- Performance optimizations
- Additional file format support
- Multi-language support
- Documentation improvements
- Bug fixes and testing

## Contact

Tomás Beck Torres - becktorrescoding@gmail.com

Website - becktorrescoding@odoo.com

Project Link: [https://github.com/becktorrescoding/image_to_pdf](https://github.com/becktorrescoding/image_to_pdf)

## Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - OCR engine
- [OCRmyPDF](https://github.com/ocrmypdf/OCRmyPDF) - PDF conversion tool
- [pytesseract](https://github.com/madmaze/pytesseract) - Python wrapper for Tesseract
- [Pillow](https://python-pillow.org/) - Python imaging library
