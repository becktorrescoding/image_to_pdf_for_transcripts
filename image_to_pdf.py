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


def convert_image(image):

    if image.exists():

        print("Converting image to pdf")



        try:

            ocrmypdf.ocr(image, output_path, deskew=True, force_ocr=True, output_type="pdf")

            print(f"File {image} converted to PDF at {output_path}")

        except Exception as e:

            print(f"Error converting {image}: {e}")

def bulk_convert( input_folder, output ):

    if not os.path.exists(input_folder):
        raise FileNotFoundError(f'{input_folder} not found.')

    for root, dirs, files in os.walk(input_folder):

        for file in files:

            image = Image.open(os.path.join(root, file))

            image.save(output)

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

        print("File found.")

        while True:

            folder_response = input("Would you like to view the image, convert it to PDF, or quit? (V/C/Q): ")

            if folder_response.lower() == "v":

                Image.open(matched_files[0]).show()

            elif folder_response.lower() == "c":

                convert_image(matched_files[0])

            elif folder_response.lower() == "q":

                break

            else:

                print("Invalid input. Try again.")


def search_fallback(folder_path, search_for):

    keywords = search_for.split()

    partial_matched_files = []

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

        print("File found.")

        while True:

            fallback_response = input("Would you like to view the image, convert it to PDF, or quit? (V/C/Q): ")

            if fallback_response.lower() == "v":

                Image.open(partial_matched_files[0]).show()

            elif fallback_response.lower() == "c":

                convert_image(partial_matched_files[0])

            elif fallback_response.lower() == "q":

                break

            else:

                print("Invalid input. Try again.")


def search_images(matched_files, date):

    files = []

    for file in matched_files:

        try:
            text = pytesseract.image_to_string(Image.open(file))

            if date.lower() in text.lower():

                files.append(file)

        except Exception as e:

            print(f"Error processing {file}: {e}")

    if len(files) == 0:

        print("No matching documents found.")

    elif len(files) > 1:

        print("More than one matching documents found.")

        print("Providing list of all matched files.")

        with open("matched files.txt", "w") as f:

            f.write("\n".join(files))

    else:

        print("File found.")

        while True:

            image_response = input("Would you like to view the image, convert it to PDF, or quit? (V/C/Q): ")

            if image_response.lower() == "v":

                Image.open(files[0]).show()

            elif image_response.lower() == "c":

                convert_image(files[0])

            elif image_response.lower() == "q":

                break

            else:

                print("Invalid input. Try again.")


if __name__ == "__main__":

    if output_path == r"" or input_path == r"":
        raise ValueError("Please provide input and output path")

    response = input("Would you like to find or bulk convert files? (f/c): ")

    if response.lower() == "f":

        name = input("Enter first and last name: ")

        search_folders(input_path, name)

    elif response.lower() == "c":

        bulk_convert(input_path, output_path)
