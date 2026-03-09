import os
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
        self.root.geometry("1000x900")
        self.root.resizable(width=False, height=False)

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
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if file.lower().endswith(self.valid_ext):
                    total_files += 1

        self.log(f"Found {total_files} image(s) to convert.")
        self.log("")

        # Convert each file
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if file.lower().endswith(self.valid_ext):
                    img_path = Path(root) / file

                    try:
                        output_file = output_folder / f"{img_path.stem}.pdf"

                        self.log(f"Converting: {file}")

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

    def search_folders(self, folder_path, search_for):  # FIXED
        """Search for exact text match"""
        matched_files = []

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(self.valid_ext):
                    img_path = os.path.join(root, file)

                    try:
                        # Use pytesseract instead of open()
                        text = pytesseract.image_to_string(Image.open(img_path))

                        if search_for.lower() in text.lower():
                            matched_files.append(img_path)  # FIXED: Full path not just filename
                            self.log(f"Match found: {file}")

                    except Exception as e:
                        self.log(f"Error processing {file}: {e}")

        return matched_files

    def search_fallback(self, folder_path, search_for):
        """Partial keyword matching"""
        keywords = search_for.split()
        partial_matched_files = []

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(self.valid_ext):
                    img_path = os.path.join(root, file)

                    try:
                        # Use pytesseract instead of open()
                        text = pytesseract.image_to_string(Image.open(img_path))
                        matched_words = [word for word in keywords if word.lower() in text.lower()]

                        if len(matched_words) >= (len(keywords) / 2) and len(keywords) > 1:
                            partial_matched_files.append(img_path)
                            self.log(f"Partial match found: {file}")

                    except Exception as e:
                        self.log(f"Error processing {file}: {e}")

        return partial_matched_files

    def convert_image(self, image_path):
        """Convert single image to PDF"""
        try:
            img_path = Path(image_path)
            output_folder = Path(self.output_path.get())
            output_file = output_folder / f"{img_path.stem}.pdf"

            self.log(f"Converting {img_path.name} to PDF...")

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
        """Filter by year"""
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
