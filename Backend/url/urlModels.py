import numpy as np
import pandas as pd
import re
from urllib.parse import urlparse
import pickle

def safe_count_special_chars(url):
    if pd.isna(url) or not isinstance(url, str):
        return 0
    return len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', str(url)))

def safe_url_length(url):
    if pd.isna(url) or not isinstance(url, str):
        return 0
    return len(str(url))

def safe_count_subdomains(url):
    if pd.isna(url) or not isinstance(url, str):
        return 0
    return len(urlparse(str(url)).netloc.split('.')) - 1

def check_url(url):
    with open('C://Users/91810/Desktop/VJTI/Backend/models/tfidf_vectorizer_new.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
        
    with open('C:\\Users\91810\Desktop\VJTI\Backend\models\svm_model_new.pkl', 'rb') as f:
        model = pickle.load(f)
        
    features = np.hstack((
        vectorizer.transform([str(url)]).toarray(),
        [[
            safe_count_special_chars(url),
            safe_url_length(url),
            safe_count_subdomains(url)
        ]]
    ))
    result = model.predict(features)[0]
    return "Phised" if result == 1 else "Legitimate"

    
    

