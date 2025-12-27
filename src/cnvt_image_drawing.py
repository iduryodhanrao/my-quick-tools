try:
    import cv2
except Exception as e:
    raise ImportError(
        "OpenCV (cv2) is required. On servers without GUI install 'opencv-python-headless' or add 'opencv-python' locally. "
        f"Original error: {e}"
    )
import numpy as np
import io
from typing import Optional


def convert_image_bytes(
    image_bytes: bytes,
    blur_ksize: int = 9,
    sigma_color: int = 75,
    sigma_space: int = 75,
    min_area: int = 100,
) -> bytes:
    """Convert input image bytes to a clean outline PNG and return PNG bytes.

    Args:
        image_bytes: raw bytes of the input image (any format readable by OpenCV)
        blur_ksize: kernel "d" parameter for bilateralFilter (odd integer >=1). Will be coerced to odd.
        min_area: minimum contour area to keep; smaller contours will be removed.

    Returns:
        PNG image bytes of the processed outline image.
    """
    # Convert bytes to numpy array for OpenCV
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Could not decode image bytes")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Ensure blur_ksize is at least 1 and odd
    if blur_ksize <= 0:
        blur_ksize = 1
    if blur_ksize % 2 == 0:
        blur_ksize += 1

    # Apply Gaussian blur first, then bilateral filter to preserve edges while reducing noise
    #blurred = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)
    # Use provided sigma_color and sigma_space for bilateral filtering
    filtered = cv2.bilateralFilter(gray, d=blur_ksize, sigmaColor=sigma_color, sigmaSpace=sigma_space)

    # Use adaptive thresholding for better edge separation
    adaptive_thresh = cv2.adaptiveThreshold(
        filtered, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        blockSize=11,
        C=2
    )

    # Optional: Morphological operations to clean up noise
    kernel = np.ones((2, 2), np.uint8)
    cleaned = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_OPEN, kernel)

    # Remove small contours (background noise) using min_area threshold
    contours, _ = cv2.findContours(cleaned.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(cleaned)
    for contour in contours:
        if cv2.contourArea(contour) >= min_area:
            cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

    # Invert the edges for a sketch effect
    inverted_edges = cv2.bitwise_not(mask)

    # Encode the result to PNG bytes
    success, png = cv2.imencode('.png', inverted_edges)
    if not success:
        raise RuntimeError('Failed to encode output image')

    return png.tobytes()


if __name__ == '__main__':
    # Quick local test when run directly: read sample file and write output
    import sys
    if len(sys.argv) > 1:
        in_path = sys.argv[1]
    else:
        in_path = r'C:\Users\Indugu Rao\Downloads\blacknwhiteAishini.jpg'

    with open(in_path, 'rb') as f:
        out_bytes = convert_image_bytes(f.read())

    out_path = '..\\output\\clean_outline.png'
    with open(out_path, 'wb') as f:
        f.write(out_bytes)
    print(f'Wrote {out_path}')


