import os
import ocrmypdf
import pytesseract
from pathlib import Path
from PIL import Image

# TODO add output folder path here
output_path = Path("")
input_path = Path("")

def convert_tiff(tiff):
    if tiff.exists():
        print("Converting image to pdf")
        ocrmypdf.ocr(tiff, output_path, deskew=True, force_ocr=True)


def search_folders(folder_path, search_for):
    matched_files = []

    # Supported image extensions
    valid_ext = ('.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.TIF', '.tiff', '.tif')

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(valid_ext):
                img_path = os.path.join(root, file)

                try:
                    # Open image and convert to text
                    text = pytesseract.image_to_string(Image.open(img_path))

                    if search_for.lower() in text.lower():
                        matched_files.append(img_path)

                        print(f"Match found: {img_path}")

                except Exception as e:
                    print(f"Error processing {img_path}: {e}")

    if len(matched_files) > 1:

        print("More than one matching documents found.")

        date = input("Enter Year of Admission (YY): ")

        search_images(matched_files, date)

    elif len(matched_files) == 0:

        print("No matching documents found. Attempting partial match of name.")
        search_fallback(folder_path, search_for)

    else:

        response = input("File found. Would you like to view or convert it to PDF? (V/C): ")

        if response.lower() == "v":

            Image.open(matched_files[0]).show()

        elif response.lower() == "c":

            convert_tiff(matched_files[0])


def search_fallback(folder_path, search_for):

    keywords = search_for.split()

    partial_matched_files = []

    valid_ext = ('.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.TIF', '.tiff', '.tif')

    for root, dirs, files in os.walk(folder_path):

        for file in files:

            if file.lower().endswith(valid_ext):

                img_path = os.path.join(root, file)

                try:
                    # Open image and convert to text
                    text = pytesseract.image_to_string(Image.open(img_path))

                    matched_words = [word for word in keywords if word.lower() in text.lower()]

                    # Threshold for "partial" match of name (50%)
                    if len(matched_words) >= (len(keywords) / 2) and len(keywords) > 1:

                        partial_matched_files.append(img_path)

                    else:

                        print(f"No matches found for {search_for}")

                except Exception as e:

                    print(f"Error processing {img_path}: {e}")

    if len(partial_matched_files) > 1:

        print("More than one matching documents found.")

        date = input("Enter Year of Admission (YY): ")

        search_images(partial_matched_files, date)

    elif len(partial_matched_files) == 0:

        print("No matching documents found.")

    else:

        response = input("File found. Would you like to view or convert it to PDF? (V/C): ")

        if response.lower() == "v":

            Image.open(partial_matched_files[0]).show()

        elif response.lower() == "c":

            convert_tiff(partial_matched_files[0])


def search_images(matched_files, date):

    files = []

    for file in matched_files:

        try:
            text = pytesseract.image_to_string(Image.open(file))

            if date.lower() in text.lower():

                files.append(file)

        except Exception as e:

            print(f"Error processing {file}: {e}")

    if len(files) == 1:

        response = input("File found. Would you like to view or convert it to PDF? (V/C): ")

        if response.lower() == "v":

            Image.open(files[0]).show()

        elif response.lower() == "c":

            convert_tiff(files[0])

    elif len(files) == 0:

        print("No matching documents found.")

    else:

        print("More than one matching documents found.")

        print("Providing list of all matched files.")

        with open("matched files.txt", "w") as f:

            f.write("\n".join(files))


if __name__ == "__main__":

    name = input("Enter first and last name: ")

    search_folders(input_path, name)
