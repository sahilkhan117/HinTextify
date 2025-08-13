import os
import cv2
from PIL import Image
import pytesseract

# ---------- CONFIG ----------
input_folder = r"Book"         # folder containing scanned images
output_folder = r"Book_text"   # folder for output text files

# Explicitly set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\hp\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# ---------- PROCESSING ----------
# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Supported image extensions
image_extensions = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp')

def preprocess_image(image_path):
    """Enhance image for better OCR."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # grayscale
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # binarization
    img = cv2.medianBlur(img, 3)  # remove noise
    return img

# Process each image
for filename in os.listdir(input_folder):
    if filename.lower().endswith(image_extensions):
        image_path = os.path.join(input_folder, filename)

        # Preprocess image
        processed_img = preprocess_image(image_path)

        # Convert to PIL for pytesseract
        pil_img = Image.fromarray(processed_img)

        # Extract Hindi text in Unicode
        text = pytesseract.image_to_string(pil_img, lang='hin')

        # Save to text file with same name as image
        text_filename = os.path.splitext(filename)[0] + ".txt"
        text_path = os.path.join(output_folder, text_filename)
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"✅ Extracted text saved: {text_filename}")

print("🎯 All images processed successfully.")
