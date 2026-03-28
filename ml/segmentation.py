import cv2
import numpy as np
import os


# -----------------------------------------
# HELPER: Safe image loader
# Works even if folder path has special
# characters (Japanese, Hindi, etc.)
# -----------------------------------------
def load_image_safe(image_path):
    """
    Loads an image safely using numpy.
    Handles non-English folder paths on Windows.

    Input  : image_path (string) — full or relative path to image
    Output : img_rgb (numpy array) — RGB image
    """

    # Read raw bytes from file — works with any folder name
    img_array = np.fromfile(image_path, dtype=np.uint8)

    # Check if file was found and read
    if len(img_array) == 0:
        raise ValueError("Image file not found. Check this path: " + image_path)

    # Decode bytes into an actual image
    img_bgr = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Check if decoding worked
    if img_bgr is None:
        raise ValueError("Image could not be decoded. Is it a valid jpg/png? Path: " + image_path)

    # Convert BGR (OpenCV default) to RGB
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    return img_rgb


# -----------------------------------------
# FUNCTION 1: Segment the wound
# Detects red/pink wound area and creates
# a black-and-white mask
# -----------------------------------------
def segment_wound(img_rgb):
    """
    Detects red/pink wound region using HSV colour thresholding.
    Uses TWO red ranges because red wraps around in HSV colour space.

    Input  : img_rgb (numpy array) — RGB image
    Output : mask (numpy array)   — binary mask, same size as input
                                    white (255) = wound pixels
                                    black (0)   = non-wound pixels
    """

    # Step 1: Convert RGB to BGR (OpenCV works in BGR internally)
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

    # Step 2: Convert BGR to HSV
    # HSV is better than RGB for detecting colours under different lighting
    # H = Hue (actual colour 0-179), S = Saturation (0-255), V = Value/brightness (0-255)
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # Step 3: Define two red colour ranges
    # WHY TWO RANGES?
    # In HSV, red colour appears at BOTH ends of the hue scale:
    #   - Lower red: hue 0 to 10
    #   - Upper red: hue 170 to 180
    # If you only use one range you will miss half the red pixels

    # Lower red range (hue 0-10)
    lower_red1 = np.array([0,   70,  50])
    upper_red1 = np.array([10, 255, 255])

    # Upper red range (hue 170-180)
    lower_red2 = np.array([170,  70,  50])
    upper_red2 = np.array([180, 255, 255])

    # Step 4: Create a mask for each red range
    # inRange() makes a white pixel wherever the colour matches, black everywhere else
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # Step 5: Combine both masks into one
    # Adding them gives white wherever EITHER mask detected red
    mask = cv2.add(mask1, mask2)

    # Step 6: Clean up the mask using morphology
    # Creates a 5x5 block of ones used as a "brush" for cleaning
    kernel = np.ones((5, 5), np.uint8)

    # MORPH_CLOSE: fills small black holes INSIDE the wound region
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # MORPH_OPEN: removes tiny white specks OUTSIDE the wound region
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    return mask


# -----------------------------------------
# FUNCTION 2: Draw boundary around wound
# Draws a green outline on the image
# wherever the wound was detected
# -----------------------------------------
def draw_boundary(img_rgb, mask):
    """
    Draws a green contour line around the detected wound region.

    Input  : img_rgb (numpy array) — original RGB image
             mask    (numpy array) — binary mask from segment_wound()
    Output : result_rgb (numpy array) — RGB image with green boundary drawn
    """

    # Work on a copy so we don't modify the original image
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

    # Find the outlines of all white regions in the mask
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,       # only find outermost outlines
        cv2.CHAIN_APPROX_SIMPLE  # store only corner points, saves memory
    )

    # If no wound was detected, return the original image unchanged
    if len(contours) == 0:
        print("  No wound contours found — returning original image.")
        return img_rgb

    # Draw all contours in green colour, thickness 2 pixels
    # -1 means draw ALL contours (not just one)
    # (0, 255, 0) is green in BGR
    cv2.drawContours(img_bgr, contours, -1, (0, 255, 0), 2)

    # Convert back to RGB before returning
    result_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    return result_rgb


# -----------------------------------------
# FUNCTION 3: Compute wound area
# Counts how many pixels are white in mask
# -----------------------------------------
def compute_area(mask):
    """
    Counts white pixels in the mask.
    Each white pixel = one pixel of detected wound.

    Input  : mask (numpy array) — binary mask from segment_wound()
    Output : area (int)         — number of wound pixels
    """

    # np.sum counts all pixels where value > 0 (i.e. white pixels)
    area = np.sum(mask > 0)

    return int(area)


# -----------------------------------------
# FUNCTION 4: Save image to disk
# -----------------------------------------
def save_image_safe(img_rgb, save_path):
    """
    Saves an RGB image to disk safely.
    Handles non-English folder paths on Windows.

    Input  : img_rgb    (numpy array) — RGB image to save
             save_path  (string)      — where to save it (e.g. "outputs/result.jpg")
    Output : nothing — just saves the file
    """

    # Convert RGB back to BGR for OpenCV saving
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

    # Encode the image into memory as JPEG bytes
    success, encoded_image = cv2.imencode(".jpg", img_bgr)

    if not success:
        print("  Warning: Could not encode image for saving.")
        return

    # Write the bytes to file using numpy — works with any path
    encoded_image.tofile(save_path)

    print("  Saved:", save_path)


# -----------------------------------------
# FUNCTION 5: Run full segmentation pipeline
# Call this one function from pipeline.py
# -----------------------------------------
def run_segmentation(image_path):
    """
    Master function — runs the full segmentation pipeline.
    This is what pipeline.py will call.

    Input  : image_path (string) — path to wound image
    Output : dict with all results
    """

    print("  Loading image...")
    img_rgb = load_image_safe(image_path)

    print("  Segmenting wound region...")
    mask = segment_wound(img_rgb)

    print("  Drawing boundary...")
    annotated_img = draw_boundary(img_rgb, mask)

    print("  Computing area...")
    area = compute_area(mask)

    print("  Wound area detected:", area, "pixels")

    return {
        "img_rgb":       img_rgb,       # original image as numpy array
        "mask":          mask,          # black-white mask
        "annotated_img": annotated_img, # image with green boundary drawn
        "wound_area":    area           # number of wound pixels (int)
    }


# -----------------------------------------
# TEST BLOCK
# This only runs when you do:
#   python segmentation.py
# It does NOT run when pipeline.py imports this file
# -----------------------------------------
if __name__ == "__main__":

    print("=" * 50)
    print("  HealTrack AI — Segmentation Module Test")
    print("=" * 50)

    # ── CHANGE THIS PATH TO YOUR IMAGE ──────────────
    # Put the actual path to your day1.jpg here
    # Use forward slashes even on Windows — safer
    IMAGE_PATH = "data/patient_001/day1.jpg"
    # ────────────────────────────────────────────────

    # Check if the file actually exists before doing anything
    if not os.path.exists(IMAGE_PATH):
        print("")
        print("ERROR: Image not found at:", IMAGE_PATH)
        print("")
        print("Things to check:")
        print("  1. Are you running this from inside the ml/ folder?")
        print("     Open terminal, type:  cd C:/healtrack/ml")
        print("     Then run:             python segmentation.py")
        print("  2. Is the file named exactly day1.jpg (not Day1.JPG)?")
        print("  3. Is it inside ml/data/patient_001/ folder?")
        print("")
    else:
        # Run the full pipeline
        result = run_segmentation(IMAGE_PATH)

        print("")
        print("── Results ──────────────────────────")
        print("  Original image shape :", result["img_rgb"].shape)
        print("  Mask shape           :", result["mask"].shape)
        print("  Wound area (pixels)  :", result["wound_area"])
        print("")

        # Create outputs folder if it doesn't exist
        os.makedirs("outputs", exist_ok=True)

        # Save the annotated image (with green boundary)
        save_image_safe(result["annotated_img"], "outputs/segmented_day1.jpg")

        # Save the raw mask as a black-white image
        cv2.imwrite("outputs/mask_day1.jpg", result["mask"])
        print("  Saved: outputs/mask_day1.jpg")

        print("")
        print("All done! Check the outputs/ folder.")
        print("=" * 50)