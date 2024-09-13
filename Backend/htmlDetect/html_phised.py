import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import pickle

def extract_features(soup, url):
    parsed_url = urlparse(url)
    filename = parsed_url.path.split('/')[-1] or 'index.html'
    features = {
        'url': url,
        'url_length': len(url),
        'num_dots_in_url': url.count('.'),
        'num_special_chars': len(re.findall(r'[@\-_=&]', url)),
        'num_subdomains': url.count('.') - 1,
        'num_forms': len(soup.find_all('form')),
        'num_inputs': len(soup.find_all('input')),
        'num_password_fields': len(soup.find_all('input', {'type': 'password'})),
        'num_external_links': len([link for link in soup.find_all('a', href=True) if urlparse(link['href']).netloc]),
        'num_internal_links': len([link for link in soup.find_all('a', href=True) if not urlparse(link['href']).netloc]),
        'num_hidden_fields': len(soup.find_all('input', {'type': 'hidden'})),
        'num_mailto_links': len(soup.find_all('a', href=re.compile(r'^mailto:'))),
        'num_scripts': len(soup.find_all('script')),
        'num_js_functions': sum([str(script).count('function') for script in soup.find_all('script')]),
        'has_eval_js': int(any('eval(' in str(script) for script in soup.find_all('script'))),
        'has_escape_js': int(any('escape(' in str(script) for script in soup.find_all('script'))),
        'has_unescape_js': int(any('unescape(' in str(script) for script in soup.find_all('script'))),
        'has_settimeout_js': int(any('setTimeout(' in str(script) for script in soup.find_all('script'))),
        'has_setinterval_js': int(any('setInterval(' in str(script) for script in soup.find_all('script'))),
        'has_https': int(url.startswith('https://')),
        'suspicious_url': int(any(keyword in url.lower() for keyword in ['login', 'bank', 'verify', 'secure', 'account'])),
        'num_meta_tags': len(soup.find_all('meta')),
        'num_refresh_meta': len(soup.find_all('meta', attrs={'http-equiv': 'refresh'})),
        'num_iframes': len(soup.find_all('iframe')),
        'num_hidden_iframes': len([iframe for iframe in soup.find_all('iframe') if iframe.get('style') == 'display:none']),
        'num_images': len(soup.find_all('img')),
        'num_images_with_suspicious_url': len([img for img in soup.find_all('img') if any(keyword in img.get('src', '').lower() for keyword in ['login', 'bank', 'verify', 'secure', 'account'])]),
        'num_style_tags': len(soup.find_all('style')),
        'num_inline_styles': len(soup.find_all(style=True)),
        'num_onload_attributes': len(soup.find_all(attrs={'onload': True})),
        'num_onerror_attributes': len(soup.find_all(attrs={'onerror': True})),
        'num_external_form_actions': len([form for form in soup.find_all('form') if urlparse(form.get('action', '')).netloc])
    }

    return features


def check_html(url):
  with open('C:/Users/91810/Desktop/VJTI/Backend/models/rf_model.pkl', 'rb') as f:
      rf = pickle.load(f)

  with open('C:/Users/91810/Desktop/VJTI/Backend/models/xgb_model.pkl', 'rb') as f:
      xgb_model = pickle.load(f)

  with open('C:/Users/91810/Desktop/VJTI/Backend/models/lgb_model.pkl', 'rb') as f:
      lgb_model = pickle.load(f)

  with open('C:/Users/91810/Desktop/VJTI/Backend/models/cat_model.pkl', 'rb') as f:
      cat_model = pickle.load(f)

  with open('C:/Users/91810/Desktop/VJTI/Backend/models/scaler.pkl', 'rb') as f:
      scaler = pickle.load(f)

  data = []
  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
  }
  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    features = extract_features(soup, url)
    data.append(features)

  except requests.exceptions.RequestException as e:
    print(f"Error fetching {url}: {e}")

  test_df = pd.DataFrame(data)
  test_df_without_url = test_df.drop('url', axis=1)
  text_url = scaler.transform(test_df_without_url)

  # Initialize counters
  safe = 0
  unsafe = 0

  models = {
      'rf': rf,
      'catboost': cat_model,
      'xgboost': xgb_model,
      'lightgbm': lgb_model
  }

  for model_name, model in models.items():
      prediction = model.predict(text_url)
      
      if prediction == 0:
          safe += 1
      else:
          unsafe += 1
    
  safe_percentage = safe*25
  return safe_percentage

