import cv2
import pytesseract
from api import get_name_list, update_grade
import difflib
import sys

def extract(image_path, coordinates, settings=None):
    image = cv2.imread(image_path)

    x, y, w, h = coordinates
    roi = image[y:y+h, x:x+w]

    if settings is None:
        text = pytesseract.image_to_string(roi, config='--psm 6')  # PSM 6 for single block of text
    else:
        text = pytesseract.image_to_string(roi, config=r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789')
    return text.strip()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 ocr.py file_path courseid \"Grade item name\"")
        exit()
    image_path = sys.argv[1]
    name = extract(image_path, (270, 90, 350, 27))
    print("Name:", name)
    surname = extract(image_path, (270, 145, 350, 27))
    print("Surname: ", surname)
    name = name + surname
    name_list = get_name_list()
    print(name_list)
    match = difflib.get_close_matches(name, name_list)
    print(match[0])
    score = extract(image_path, (725, 85, 100, 50), 1)
    print("Score: ", score)
    update_grade(match[0], sys.argv[3], score)