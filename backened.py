import cv2
import numpy as np

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_deepfake(image_path):
    # Load and validate the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found or cannot be opened!")
        return "Error"

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) == 0:
        return "No Face Detected"

    fake_votes = 0  # Count fake detections
    total_checks = 0

    for (x, y, w, h) in faces:
        face_roi = image[y:y+h, x:x+w]

        # Apply all deepfake detection techniques
        total_checks += 1
        fake_votes += skin_color_analysis(face_roi)
        fake_votes += lighting_inconsistency(face_roi)
        fake_votes += blur_detection(face_roi)
        fake_votes += edge_analysis(face_roi)
        fake_votes += noise_analysis(face_roi)

    # If more than 60% of checks flag it as fake, classify it as fake
    if fake_votes / total_checks > 0.6:
        return "Fake"
    return "Real"

# **1️⃣ Skin Color Analysis (Detects unusual skin tone variation)**
def skin_color_analysis(face_roi):
    hsv = cv2.cvtColor(face_roi, cv2.COLOR_BGR2HSV)
    skin_mask = cv2.inRange(hsv, (0, 40, 50), (30, 255, 255))
    skin = cv2.bitwise_and(face_roi, face_roi, mask=skin_mask)
    
    hist = cv2.calcHist([skin], [0], None, [256], [0, 256])
    skin_tone_variation = np.std(hist)  # Measure variation in skin tone

    threshold = np.mean(hist) * 0.2  # Dynamic threshold
    return 1 if skin_tone_variation < threshold else 0

# **2️⃣ Lighting Inconsistency (Detects uneven brightness)**
def lighting_inconsistency(face_roi):
    left_half = face_roi[:, :face_roi.shape[1]//2]
    right_half = face_roi[:, face_roi.shape[1]//2:]

    left_brightness = np.mean(cv2.cvtColor(left_half, cv2.COLOR_BGR2GRAY))
    right_brightness = np.mean(cv2.cvtColor(right_half, cv2.COLOR_BGR2GRAY))

    brightness_diff = abs(left_brightness - right_brightness)
    threshold = np.std(cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)) * 0.5  # Dynamic threshold
    return 1 if brightness_diff > threshold else 0

# **3️⃣ Blurriness Detection (Detects unnatural sharpness)**
def blur_detection(face_roi):
    variance = cv2.Laplacian(face_roi, cv2.CV_64F).var()
    threshold = np.mean(cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)) * 0.5  # Dynamic threshold
    return 1 if variance < threshold else 0

# **4️⃣ Edge Analysis (Detects unnatural smooth edges)**
def edge_analysis(face_roi):
    edges = cv2.Canny(face_roi, 100, 200)
    edge_ratio = np.count_nonzero(edges) / (face_roi.shape[0] * face_roi.shape[1])

    threshold = 0.01  # Fine-tuned for better accuracy
    return 1 if edge_ratio < threshold else 0

# **5️⃣ Noise Analysis (Detects fake noise patterns)**
def noise_analysis(face_roi):
    noise = cv2.fastNlMeansDenoisingColored(face_roi, None, 10, 10, 7, 21)
    noise_diff = np.mean(cv2.absdiff(face_roi, noise))

    threshold = np.std(cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)) * 0.8  # Dynamic threshold
    return 1 if noise_diff > threshold else 0

# **Test the deepfake detector**
image_path = "test_image.png"  # Change this to your image path
result = detect_deepfake(image_path)
print("Deepfake Detection Result:", result)
