from PIL import Image
import pytesseract
import easyocr
import argparse
import cv2 # opencv

def main(image_path, method):    

    if method == 'tesseract':
        print("Starting Tesseract scan...")
        img = cv2.imread(image_path)
        # Removes color variation and focuses OCR on text contrast
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Resize (very important for OCR accuracy)
        gray = cv2.resize(
            gray,
            None,
            fx=2,
            fy=2,
            interpolation=cv2.INTER_CUBIC
        )
        # Noise removal
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # If uneven lighting, turn text black with white BG
        # thresh = cv2.adaptiveThreshold(
        #     gray,
        #     255,
        #     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #     cv2.THRESH_BINARY,
        #     31,
        #     2
        # )
        
        # This is for when text is clean scan (Otsu threshold)
        _, thresh = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        # Invert image if needed
        # thresh = cv2.bitwise_not(thresh)

        # Debug input before tesseract
        cv2.imshow("OCR Input", thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Fix tilted scans
        # coords = cv2.findNonZero(thresh)
        # angle = cv2.minAreaRect(coords)[-1]

        text = pytesseract.image_to_string(thresh, config="--psm 6")
        print(text)

    else:
        print("Starting EasyOCR scan...")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # Light denoise only
        gray = cv2.fastNlMeansDenoising(gray, h=10)

        reader = easyocr.Reader(["en"])
        results = reader.readtext(gray)

        for bbox, text, conf in results:
            print(f"{conf:.2f} | {text}")
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, required=True, help="Path to image")
    parser.add_argument("--method", type=str, default='tesseract', help="OCR Method to use: tesseract | easyocr")
    args = parser.parse_args()
    
    main(args.path)
