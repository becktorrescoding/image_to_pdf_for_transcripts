import os
import ocrmypdf
import pytesseract
from pathlib import Path
from PIL import Image

# Global Variables

valid_ext = ('.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.TIF', '.tiff', '.tif')

# TODO add input & output folder paths here
output_path = Path(r"")
input_path = Path(r"")


def convert_tiff(tiff):

    if tiff.exists():

        print("Converting image to pdf")

        try:

            ocrmypdf.ocr(tiff, output_path, deskew=True, force_ocr=True)

            print(f"File {tiff} converted to PDF at {output_path}")

        except Exception as e:

            print(f"Error converting {tiff}: {e}")

def bulk_convert( input, output ):

    if not os.path.exists(input):
        raise FileNotFoundError(f'{input} not found.')

    for dirs, files in os.walk(input):

        for file in files:

            image = Image.open(os.path.join(input, file))

            image.save( os.path.join(output, os.path.splitext(file)[0]), format="PDF" )

def search_folders(folder_path, search_for):

    matched_files = []

    for root, dirs, files in os.walk(folder_path):

        for file in files:

            if file.lower().endswith(valid_ext):

                img_path = os.path.join(root, file)

                try:
                    # Open image and convert to text
                    image = Image.open(img_path)
                    text = pytesseract.image_to_string(image)

                    if search_for.lower() in text.lower():

                        matched_files.append(image)

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
                    image = Image.open(img_path)
                    text = pytesseract.image_to_string(image)

                    matched_words = [word for word in keywords if word.lower() in text.lower()]

                    # Threshold for "partial" match of name (50%)
                    if len(matched_words) >= (len(keywords) / 2) and len(keywords) > 1:

                        partial_matched_files.append(image)

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

    response = input("Would you like to find or bulk convert files? (f/c): ")

    if response.lower() == "f":

        name = input("Enter first and last name: ")

        search_folders(input_path, name)

    elif response.lower() == "c":

        bulk_convert(input_path, output_path)
