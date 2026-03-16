import os
import re
import ocrmypdf
import pytesseract
from PIL import Image
from pathlib import Path
import tkinter as tk
import threading
from tkinter import filedialog, messagebox, scrolledtext

class ImageToPDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        self.root.geometry("700x600")
        self.root.resizable(width=True, height=True)

        # Variables
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.search_name = tk.StringVar()
        self.search_year = tk.StringVar()
        self.mode = tk.StringVar(value="search")  # ADDED for mode selection
        self.valid_ext = ('.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.TIF', '.tiff', '.tif')

        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="Image to PDF Converter",
            font=("Arial", 14, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10
        )
        title.pack(fill="x")

        # Path Selection
        path_frame = tk.Frame(self.root, padx=20, pady=10)
        path_frame.pack(fill="x")

        tk.Label(path_frame, text="Input Folder:").grid(row=0, column=0, sticky=tk.W, pady=5)
        tk.Entry(path_frame, textvariable=self.input_path, width=40).grid(row=0, column=1, padx=5)
        tk.Button(path_frame, text="Browse", command=self.browse_input).grid(row=0, column=2)

        tk.Label(path_frame, text="Output Folder:").grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(path_frame, textvariable=self.output_path, width=40).grid(row=1, column=1, padx=5)
        tk.Button(path_frame, text="Browse", command=self.browse_output).grid(row=1, column=2)

        # Mode Selection
        mode_frame = tk.LabelFrame(
            self.root,
            text="Operation Mode",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10
        )
        mode_frame.pack(fill="x", padx=20, pady=(0, 10))

        tk.Radiobutton(
            mode_frame,
            text="Search Mode - Find specific documents by name",
            variable=self.mode,
            value="search",
            command=self.toggle_mode,
            font=("Arial", 9)
        ).pack(anchor="w", pady=3)

        tk.Radiobutton(
            mode_frame,
            text="Bulk Convert Mode - Convert all images to PDFs",
            variable=self.mode,
            value="bulk",
            command=self.toggle_mode,
            font=("Arial", 9)
        ).pack(anchor="w", pady=3)

        # Search Options Frame
        self.search_frame = tk.Frame(self.root, padx=20, pady=10)
        self.search_frame.pack(fill="x")

        tk.Label(self.search_frame, text="Search Name:", font=("Arial", 9)).grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(self.search_frame, textvariable=self.search_name, width=30).grid(row=0, column=1, padx=5, sticky="w")

        tk.Label(self.search_frame, text="Year (Optional):", font=("Arial", 9)).grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(self.search_frame, textvariable=self.search_year, width=10).grid(row=1, column=1, padx=5, sticky="w")

        # Start Button
        self.start_button = tk.Button(
            self.root,
            text="Start Search",
            command=self.start_search,  # YOUR function name
            bg="green",
            fg="white",
            font=("Arial", 11, "bold"),
            width=20,
            height=2
        )
        self.start_button.pack(pady=5)

        # Processing Log
        log_frame = tk.Frame(self.root, padx=20, pady=10)
        log_frame.pack(fill="both", expand=True)

        tk.Label(log_frame, text="Processing Log:", font=("Arial", 10, "bold")).pack(anchor="w")

        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=70)
        self.log_text.pack(fill="both", expand=True)

    def toggle_mode(self):
        """Show/hide search options based on mode"""
        if self.mode.get() == "bulk":
            self.search_frame.pack_forget()
        else:
            self.search_frame.pack(fill="x", padx=20, pady=10, before=self.start_button)

    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def browse_input(self):
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_path.set(folder)

    def browse_output(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_path.set(folder)

    def start_search(self):
        """Validate inputs and start processing"""
        input_folder = self.input_path.get()
        output_folder = self.output_path.get()

        # Basic validation for all modes
        if not input_folder or not output_folder:
            messagebox.showerror("Error", "Please select both input and output folders.")
            return

        # Mode-specific validation
        if self.mode.get() == "search":
            name = self.search_name.get()
            if not name:
                messagebox.showerror("Error", "Please enter a name to search for.")
                return

        # Start processing in thread
        self.start_button.config(state="disabled")

        thread = threading.Thread(target=self.do_search)  # YOUR function name
        thread.daemon = True
        thread.start()

    def do_search(self):
        """Route to correct mode and handle errors"""
        try:
            if self.mode.get() == "search":
                self.search_mode()
            else:
                self.bulk_convert_mode()

        except Exception as e:
            self.log(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))

        finally:
            self.start_button.config(state="normal")

    def search_mode(self):
        """Search for specific documents"""
        self.log("=== Starting Search Mode ===")

        input_folder = self.input_path.get()
        name = self.search_name.get()
        year = self.search_year.get()

        self.log(f"Searching for {name}")
        matched_files = self.search_folders(input_folder, name)

        if not matched_files:
            self.log("No exact matches found. Trying partial match...")
            matched_files = self.search_fallback(input_folder, name)

        if year and matched_files:
            self.log(f"Filtering by year: {year}")
            matched_files = self.search_images(matched_files, year)

        if matched_files:
            self.log(f"Found {len(matched_files)} matching file(s).")
            self.convert_image(matched_files[0])
            self.log("Search and conversion complete!")
            messagebox.showinfo("Success", "Image successfully converted to PDF")
        else:
            self.log("No matching files found.")
            messagebox.showinfo("No Results", "No matching documents found.")

    def bulk_convert_mode(self):
        """Convert all images to PDFs"""
        self.log("=== Starting Bulk Convert Mode ===")

        input_folder = Path(self.input_path.get())
        output_folder = Path(self.output_path.get())

        if not input_folder.exists():
            raise FileNotFoundError(f"Input folder not found: {input_folder}")

        converted = 0
        errors = 0
        total_files = 0

        # Count files
        for root, dirs, files in os.walk(input_folder, followlinks=False):
            for file in files:
                if file.lower().endswith(self.valid_ext):
                    total_files += 1

        self.log(f"Found {total_files} image(s) to convert.")
        self.log("")

        # Convert each file
        for root, dirs, files in os.walk(input_folder, followlinks=False):
            for file in files:
                if file.lower().endswith(self.valid_ext):
                    img_path = Path(root) / file

                    try:
                        self.log(f"Converting: {file}")

                        # Extract text and generate structured filename
                        img = Image.open(img_path)
                        name = pytesseract.image_to_string(img.crop((337, 203, 727, 261)))
                        date = pytesseract.image_to_string(img.crop((1446, 335, 1817, 596)))
                        degree = pytesseract.image_to_string(img.crop((1049, 464, 1600, 548)))
                        output_stem = self.generate_filename(name, date, degree, img_path.stem)
                        output_file = output_folder / f"{output_stem}.pdf"

                        # Avoid overwriting existing files
                        counter = 1
                        while output_file.exists():
                            output_file = output_folder / f"{output_stem}_{counter}.pdf"
                            counter += 1

                        ocrmypdf.ocr(
                            img_path,
                            output_file,
                            deskew=True,
                            force_ocr=True,
                            output_type="pdf"
                        )

                        converted += 1
                        self.log(f"  ✓ Success ({converted}/{total_files})")
                        self.log("")

                    except Exception as e:
                        errors += 1
                        self.log(f"  ✗ Error: {str(e)}")
                        self.log("")

        # Summary
        self.log("=" * 50)
        self.log(f"Bulk conversion complete!")
        self.log(f"Successfully converted: {converted}/{total_files}")
        self.log(f"Errors: {errors}")
        self.log("=" * 50)

        messagebox.showinfo("Complete", f"Converted {converted} of {total_files} file(s).\n{errors} error(s).")

    def search_folders(self, folder_path, search_for):
        """Search for exact text match with progress indicator."""
        matched_files = []

        all_files = [
            os.path.join(root, file)
            for root, dirs, files in os.walk(folder_path, followlinks=False)
            for file in files
            if file.lower().endswith(self.valid_ext)
        ]
        total = len(all_files)
        self.log(f"Scanning {total} file(s)...")

        for i, img_path in enumerate(all_files, start=1):
            file = os.path.basename(img_path)
            self.log(f"  Scanning {i}/{total}: {file}")
            try:
                text = pytesseract.image_to_string(Image.open(img_path))
                if search_for.lower() in text.lower():
                    matched_files.append(img_path)
                    self.log(f"  ✓ Match found: {file}")
            except Exception as e:
                self.log(f"  ✗ Error processing {file}: {e}")

        return matched_files

    def search_fallback(self, folder_path, search_for):
        """Partial keyword matching with progress indicator."""
        keywords = search_for.split()
        partial_matched_files = []

        all_files = [
            os.path.join(root, file)
            for root, dirs, files in os.walk(folder_path, followlinks=False)
            for file in files
            if file.lower().endswith(self.valid_ext)
        ]
        total = len(all_files)
        self.log(f"Scanning {total} file(s) for partial matches...")

        for i, img_path in enumerate(all_files, start=1):
            file = os.path.basename(img_path)
            self.log(f"  Scanning {i}/{total}: {file}")
            try:
                text = pytesseract.image_to_string(Image.open(img_path))
                matched_words = [word for word in keywords if word.lower() in text.lower()]
                if len(matched_words) >= (len(keywords) / 2) and len(keywords) > 1:
                    partial_matched_files.append(img_path)
                    self.log(f"  ✓ Partial match found: {file}")
            except Exception as e:
                self.log(f"  ✗ Error processing {file}: {e}")

        return partial_matched_files

    def generate_filename(self, name, date, degree, fallback_stem):
        """
        Generate a structured filename from OCR text.

        Degree format:    LastName_FirstName_MI_Degree_DateOfGraduation
        Transcript format: LastName_FirstName_MI_Transcript_DateOfAdmission

        Falls back to original filename if fields cannot be extracted.
        """

        def clean(value):
            """Remove characters that are invalid in filenames."""
            return re.sub(r'[\\/*?:"<>|,]', '', value).strip()

        # --- Detect document type ---
        is_degree = bool(re.search(r'degree\s+received', degree, re.IGNORECASE))
        is_transcript = bool(re.search(r'date\s+of\s+admission', date, re.IGNORECASE))

        if not is_degree and not is_transcript:
            self.log(f"  ⚠ Could not detect document type — using original filename.")
            return fallback_stem

        doc_type = "Degree" if is_degree else "Transcript"

        # --- Extract name ---
        # Tries "Last, First MI" format first, then "First MI Last"
        last, first, middle = "", "", ""

        # Format 1: Last, First [MI]
        name_match = re.search(
            r'\b([A-Z][a-zA-Z\'\-]+),\s+([A-Z][a-zA-Z\'\-]+)(?:\s+([A-Z])\.?)?',
            name
        )
        if name_match:
            last  = name_match.group(1)
            first = name_match.group(2)
            middle = name_match.group(3) or ""
        else:
            # Format 2: First [MI] Last
            name_match = re.search(
                r'\b([A-Z][a-zA-Z\'\-]+)(?:\s+([A-Z])\.?)?\s+([A-Z][a-zA-Z\'\-]+)\b',
                name
            )
            if name_match:
                first  = name_match.group(1)
                middle = name_match.group(2) or ""
                last   = name_match.group(3)

        if not last or not first:
            self.log(f"  ⚠ Could not extract name — using original filename.")
            return fallback_stem

        # --- Extract degree (only for degree documents) ---
        degree_name = ""
        if is_degree:
            degree_match = re.search(
                r'degree\s+received[:\s]+([A-Za-z\s]+?)(?:\n|$)',
                degree,
                re.IGNORECASE
            )
            if degree_match:
                degree_name = clean(degree_match.group(1)).replace(" ", "_")
            else:
                self.log(f"  ⚠ Could not extract degree name.")

        # --- Extract date ---
        # Matches "June 12, 1979", "Jun 12 1979", "06/12/79", "06/12/1979"
        MONTH_NAME = (
            r'(?:January|February|March|April|May|June|July|August|'
            r'September|October|November|December|'
            r'Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
        )
        DATE_NAMED   = MONTH_NAME + r'\s+\d{1,2},?\s+\d{4}'
        DATE_NUMERIC = r'\d{1,2}/\d{1,2}/\d{2,4}'

        MONTH_MAP = {
            'jan': 'January', 'feb': 'February', 'mar': 'March',
            'apr': 'April',   'may': 'May',       'jun': 'June',
            'jul': 'July',    'aug': 'August',     'sep': 'September',
            'oct': 'October', 'nov': 'November',   'dec': 'December'
        }

        def normalise_date(raw):
            """Convert any matched date string to Month_DD_YYYY."""
            raw = raw.strip()
            # Numeric format: mm/dd/yy or mm/dd/yyyy
            numeric = re.match(r'(\d{1,2})/(\d{1,2})/(\d{2,4})$', raw)
            if numeric:
                month_num, day, year = int(numeric.group(1)), numeric.group(2), numeric.group(3)
                if len(year) == 2:
                    year = '19' + year if int(year) >= 20 else '20' + year
                month_name = list(MONTH_MAP.values())[month_num - 1]
                return f"{month_name}_{day}_{year}"
            # Named format: "June 12, 1979" or "Jun 12 1979"
            parts = raw.replace(',', '').split()
            if len(parts) == 3:
                month_abbr = parts[0][:3].lower()
                month_name = MONTH_MAP.get(month_abbr, parts[0])
                return f"{month_name}_{parts[1]}_{parts[2]}"
            return clean(raw).replace(' ', '_')

        date = ""
        if is_degree:
            # Date of graduation appears to the right of the degree on the same line
            date_match = re.search(
                r'degree\s+received[^\n]*?(' + DATE_NAMED + r'|' + DATE_NUMERIC + r')',
                date,
                re.IGNORECASE
            )
        else:
            # Date of admission appears under "Date of Admission" label
            date_match = re.search(
                r'date\s+of\s+admission[:\s]+(' + DATE_NAMED + r'|' + DATE_NUMERIC + r')',
                date,
                re.IGNORECASE
            )

        if date_match:
            date = normalise_date(date_match.group(1))
        else:
            self.log(f"  ⚠ Could not extract date.")

        # --- Assemble filename ---
        parts = [last, first]
        if middle:
            parts.append(middle)
        if is_degree and degree_name:
            parts.append(degree_name)
        else:
            parts.append(doc_type)
        if date:
            parts.append(date)

        filename = "_".join(clean(p) for p in parts)
        self.log(f"  📄 Generated filename: {filename}.pdf")
        return filename

    def convert_image(self, image_path):
        """Convert single image to PDF with auto-generated filename."""
        try:
            img_path = Path(image_path)
            output_folder = Path(self.output_path.get())

            self.log(f"Converting {img_path.name} to PDF...")

            # Extract text and generate filename
            img = Image.open(img_path)
            name = pytesseract.image_to_string(img.crop((337, 203, 727, 261)))
            date = pytesseract.image_to_string(img.crop((1446, 335, 1817, 596)))
            degree = pytesseract.image_to_string(img.crop((1049, 464, 1600, 548)))
            output_stem = self.generate_filename(name, date, degree, img_path.stem)
            output_file = output_folder / f"{output_stem}.pdf"

            # Avoid overwriting existing files
            counter = 1
            while output_file.exists():
                output_file = output_folder / f"{output_stem}_{counter}.pdf"
                counter += 1

            ocrmypdf.ocr(
                img_path,
                output_file,
                deskew=True,
                force_ocr=True,
                output_type="pdf"
            )

            self.log(f"✓ Successfully converted to: {output_file.name}")

        except Exception as e:
            self.log(f"✗ Error converting {image_path}: {e}")

    def search_images(self, matched_files, date):
        """Filter by year - This one was correct!"""
        files = []

        for file in matched_files:
            try:
                text = pytesseract.image_to_string(Image.open(file))

                if date.lower() in text.lower():
                    files.append(file)

            except Exception as e:
                self.log(f"Error processing {file}: {e}")

        return files


def main():
    root = tk.Tk()
    app = ImageToPDFApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
