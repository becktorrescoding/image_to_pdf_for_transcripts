# Image to PDF Converter & OCR Search Tool

A Python GUI application that combines OCR-based document search with image-to-PDF conversion capabilities. Features an intuitive graphical interface that allows users to search through image files and PDFs using Optical Character Recognition (OCR) to find documents containing specific text patterns, then convert them to searchable PDFs. Particularly useful for locating and processing patient records or documents by name without needing to edit code.

## Features

- **Graphical User Interface**: Easy-to-use GUI built with tkinter - no code editing required
- **Folder Browser**: Browse and select input/output folders with native file dialogs
- **OCR Text Search**: Searches through images and PDFs using Tesseract OCR
- **Multiple Format Support**: Handles PDF, JPG, JPEG, PNG, BMP, and TIFF files
- **Fuzzy Matching**: Falls back to partial name matching (50% threshold) if exact match fails
- **Year Filtering**: Optional field to refine search results by admission year
- **Real-time Logging**: Processing status displayed in scrollable log window
- **PDF Generation**: Converts matched documents to searchable PDFs using OCRmyPDF
- **Threaded Processing**: Non-blocking operations keep GUI responsive during long tasks
- **Recursive Search**: Searches through entire directory structures
- **User-Friendly**: Clear error messages and success notifications

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
   pip install -r requirements.txt
   ```
   Or manually:
   ```bash
   pip install ocrmypdf pytesseract pillow
   ```

4. **Launch the GUI:**
   ```bash
   python image_to_pdf_gui.py
   ```

## Screenshots

### Main Interface
The application features a clean, intuitive interface:
- **Folder Selection**: Browse buttons for easy path selection
- **Search Fields**: Name and optional year input
- **Processing Log**: Real-time status updates in scrollable text area
- **Green Start Button**: Initiates the search and conversion process

### Typical Workflow
1. Select input folder containing scanned images
2. Select output folder for converted PDFs
3. Enter patient/document name
4. (Optional) Enter 2-digit year for filtering
5. Click "Start Search"
6. Monitor progress in log window
7. Receive success notification when complete

## Configuration

**No configuration needed!** The GUI allows you to select folders through browse dialogs at runtime. Simply:

1. Launch the application
2. Click "Browse" to select your input folder (where images are located)
3. Click "Browse" to select your output folder (where PDFs will be saved)
4. Enter search criteria and click "Start Search"

**Optional**: If you want to set default paths in the code, edit `image_to_pdf_gui.py`:
- Line 17-18: Modify `self.input_path` and `self.output_path` initialization

For advanced users who prefer command-line interface, see `image_to_pdf.py` (requires manual path configuration).

## Usage

### Running the Application

```bash
python image_to_pdf_gui.py
```

A graphical window will open with the following interface:

---

### Step-by-Step Usage

#### 1. Select Folders
- **Input Folder**: Click "Browse" next to "Input Folder" and select the folder containing your images
- **Output Folder**: Click "Browse" next to "Output Folder" and select where you want PDFs saved

#### 2. Enter Search Criteria
- **Search Name**: Type the first and last name to search for (e.g., "John Smith")
- **Year (Optional)**: Enter a 2-digit year (e.g., "24") to filter results. Leave blank to skip year filtering.

#### 3. Start Processing
Click the green **"Start Search"** button to begin.

#### 4. Monitor Progress
The Processing Log window shows real-time status:
```
Searching for John Smith in C:/Documents/Images
Match found: scan_001.jpg
No exact matches found. Trying partial match...
Partial match found: scan_002.jpg
Filtering by year: 24
Found 1 file(s). Converting...
Converting scan_002.jpg to PDF...
✓ Successfully converted to: scan_002.pdf
Search Complete.
```

#### 5. Results
- Success message box appears when conversion is complete
- Converted PDF is saved to your output folder
- If no matches found, you'll see an informational message

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

### Example Workflow

**Scenario**: Find and convert a patient record for "Jane Doe" from 2024

1. Launch app: `python image_to_pdf_gui.py`
2. Browse to: `C:/Hospital/Scans`
3. Browse output to: `C:/Hospital/Converted`
4. Enter name: `Jane Doe`
5. Enter year: `24`
6. Click "Start Search"
7. Wait for completion message
8. Find PDF at: `C:/Hospital/Converted/scan_xyz.pdf`

## How It Works

### GUI Architecture

The application uses a **class-based tkinter GUI** with the following structure:

```
ImageToPDFApp (Main Class)
├── __init__()           # Initialize window and variables
├── create_widgets()     # Build GUI interface
├── browse_input()       # Handle input folder selection
├── browse_output()      # Handle output folder selection
├── start_search()       # Validate inputs and start thread
├── do_search()          # Main search workflow (runs in thread)
├── search_folders()     # Exact text match via OCR
├── search_fallback()    # Partial keyword matching
├── search_images()      # Filter by year
├── convert_image()      # Convert to searchable PDF
└── log()                # Display messages in GUI
```

### Search Workflow

1. **User Input**: User enters search criteria via GUI fields
2. **Validation**: System checks all required fields are filled
3. **Threading**: Search runs in background thread (GUI stays responsive)
4. **OCR Processing**: Each image is processed with Tesseract OCR
5. **Text Matching**: Extracted text is compared against search criteria
6. **Fallback**: If no exact match, automatically tries partial matching
7. **Filtering**: Optional year filter applied if provided
8. **Conversion**: Matched file(s) converted to PDF with OCRmyPDF
9. **Notification**: User notified of success/failure

### Technical Details

- **OCR Engine**: Tesseract (via pytesseract) extracts text from images
- **PDF Creation**: OCRmyPDF creates searchable PDFs with deskewing
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

### Success Case
- **Searchable PDF**: Converted document saved to output folder with original filename + `.pdf`
- **Log Messages**: Real-time progress shown in GUI log window
- **Success Dialog**: Pop-up notification confirms completion
- **OCR Enhancement**: OCRmyPDF applies deskewing and forced OCR for improved readability

### Example Output
```
Input:  C:/Documents/scan_12345.jpg
Output: C:/Converted/scan_12345.pdf
```

### No Matches Case
- **Informational Dialog**: "No matching files found" message
- **Log Details**: Shows search attempts and why no matches were found

### Error Case
- **Error Dialog**: Specific error message displayed
- **Log Details**: Full error traceback in log window for debugging

## Error Handling

The GUI includes comprehensive error handling:

### Input Validation
- **Empty Fields**: "Please enter all required fields" dialog if name or paths missing
- **Invalid Paths**: System validates folder existence before processing
- **Clear Messaging**: Specific error messages guide user to fix issues

### Processing Errors
- **OCR Failures**: Logged with filename and error details
- **Image Read Errors**: Skips corrupted files, continues processing others
- **Conversion Errors**: Detailed error message with troubleshooting hints

### User Experience
- **Non-blocking Errors**: GUI remains responsive even during errors
- **Error Logs**: All errors displayed in log window for review
- **Graceful Degradation**: Partial matches attempted if exact match fails

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Please enter all required fields" | Missing name or folder paths | Fill in all required fields |
| "Error processing [file]" | Corrupted or unreadable image | Check image file integrity |
| "No matching files found" | No documents contain search text | Verify spelling, try partial match |
| Tesseract error | OCR engine not installed | Install Tesseract OCR |

## Limitations

- **OCR Accuracy**: Depends on image quality, text clarity, and scan resolution
- **Processing Speed**: Large directories or high-resolution images can be slow
- **Network Drives**: May be slower than local storage; consider copying files locally first
- **Partial Match Threshold**: Fixed at 50% of keywords (not user-configurable in GUI)
- **Single File Conversion**: Currently converts only the first matched file
- **Year Format**: Only supports 2-digit year format (YY), not 4-digit (YYYY)
- **GUI Responsiveness**: During OCR processing, only log updates; button disabled until complete
- **Memory Usage**: Processing very large images may consume significant RAM

## Troubleshooting

### GUI Won't Open
**Symptom**: Double-clicking does nothing or window appears then closes
**Solutions**:
- Run from terminal to see error messages: `python image_to_pdf_gui.py`
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

### No Matches Found
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

### "Please enter all required fields" Error
**Symptom**: Error even though fields look filled
**Solutions**:
- Folders must be selected via Browse button
- Name field cannot be empty
- Try clearing and re-entering information

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
- **Save/Load Settings**: Remember last used folders
- **Theme Selection**: Light/dark mode options
- **Progress Bar**: Visual progress indicator during processing
- **Drag & Drop**: Drop files directly into window
- **Multi-file Selection**: Convert multiple matched files at once
- **Preview Pane**: Show thumbnail of found images before converting

### Functionality
- **Bulk Convert Mode**: Add radio button to convert all files in folder
- **Advanced Search**: Search by multiple criteria (name AND date range)
- **Custom Match Threshold**: Slider to adjust partial match percentage
- **Four-digit Years**: Support YYYY format in addition to YY
- **Export Results**: Save list of matched files to CSV/Excel
- **Batch Processing**: Queue multiple searches to run sequentially

### Performance
- **Parallel Processing**: Multi-threaded conversion for multiple files
- **Image Caching**: Cache OCR results to speed up repeated searches
- **Smart Scanning**: Skip previously scanned files
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

Project Link: [https://github.com/yourusername/image-to-pdf-ocr](https://github.com/yourusername/image-to-pdf-ocr)

## Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - OCR engine
- [OCRmyPDF](https://github.com/ocrmypdf/OCRmyPDF) - PDF conversion tool
- [pytesseract](https://github.com/madmaze/pytesseract) - Python wrapper for Tesseract
- [Pillow](https://python-pillow.org/) - Python imaging library
