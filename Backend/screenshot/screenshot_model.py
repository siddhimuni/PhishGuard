import numpy as np
import pandas as pd
import joblib
import cv2
from PIL import Image
import imagehash
from skimage.feature import local_binary_pattern
from tensorflow.keras.models import load_model

def extract_color_histogram(img_path, bins=(8, 8, 8)):
    image = cv2.imread(img_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1, 2], None, bins, [0, 180, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist

def extract_wavelet_hash(img_path):
    img = Image.open(img_path)
    hash = imagehash.whash(img)
    return np.array(hash.hash).flatten()

def extract_sift_features(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(gray, None)
    return descriptors.flatten() if descriptors is not None else np.array([])

def extract_lbp_features(img_path):
    image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    lbp = local_binary_pattern(image, P=8, R=1, method='uniform')
    lbp_hist, _ = np.histogram(lbp, bins=np.arange(0, 11), range=(0, 10))
    return lbp_hist

def extract_orb_features(img_path):
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(gray, None)
    return descriptors.flatten() if descriptors is not None else np.array([])

def calculate_mean(array):
    if isinstance(array, list):
        array = np.array(array)
    if array.size == 0:
        return 0
    return np.mean(array)

def count_true_values(bool_list):
    return sum(bool_list)


def check_image():
    test_image = r'c:/Users/91810/Desktop/VJTI/Backend/screenshot/screenshot.png'

    scaler = joblib.load('c:/Users/91810/Desktop/VJTI/Backend/screenshot/scaler.pkl')
    rf_model = joblib.load('c:/Users/91810/Desktop/VJTI/Backend/screenshot/random_forest_model.pkl')
    model_cnn = load_model('c:/Users/91810/Desktop/VJTI/Backend/screenshot/cnn_model.h5')

    color_hist_features = extract_color_histogram(test_image)
    wavelet_hash_features = extract_wavelet_hash(test_image)
    lbp_features = extract_lbp_features(test_image)
    orb_features = extract_orb_features(test_image)
    sift_features = extract_sift_features(test_image)

    test_data = pd.DataFrame({
        'color_hist_features': [color_hist_features],
        'wavelet_hash_features': [wavelet_hash_features],
        'lbp_features': [lbp_features],
        'orb_features': [orb_features],
        'sift_features': [sift_features]
    })

    test_data['color_hist_features'] = test_data['color_hist_features'].apply(calculate_mean)
    test_data['wavelet_hash_features'] = test_data['wavelet_hash_features'].apply(count_true_values)
    test_data['lbp_features'] = test_data['lbp_features'].apply(calculate_mean)
    test_data['orb_features'] = test_data['orb_features'].apply(calculate_mean)
    test_data['sift_features'] = test_data['sift_features'].apply(calculate_mean)

    X_test_image = test_data[['color_hist_features', 'wavelet_hash_features', 'lbp_features', 'orb_features', 'sift_features']]
    X_test_image_scaled = scaler.transform(X_test_image)
    X_test_image_scaled = X_test_image_scaled.reshape((X_test_image_scaled.shape[0], X_test_image_scaled.shape[1], 1))
    rf_preds = rf_model.predict(X_test_image_scaled.reshape(X_test_image_scaled.shape[0], -1))
    cnn_preds = model_cnn.predict(X_test_image_scaled).flatten()

    final_preds = (rf_preds + cnn_preds) / 2
    final_preds = (final_preds > 0.5).astype(int)
    return "Phised" if final_preds[0]==1 else "Legitimate"
