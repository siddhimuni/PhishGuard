from flask import Flask, request, jsonify
from htmlDetect.html_phised import check_html
from flask_cors import CORS
from url.urlModels import check_url
from screenshot.screenshot_model import check_image
import base64

app = Flask(__name__)
CORS(app)

@app.route('/htmlPhished', methods=['POST'])
def htmlPhished():
    data = request.get_json()
    url = data.get("url")
    return jsonify(check_html(url))


@app.route('/urlDetection', methods=['POST'])
def urlDetection():
    data = request.get_json()
    url = data.get("url")
    return jsonify(check_url(url))


@app.route('/screenshotDetection', methods=['POST'])
def screenshotDetection():
    data = request.get_json()
    image_data = data.get('image')
    
    image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)

    with open('C:\\Users\91810\Desktop\VJTI\Backend\screenshot\screenshot.png', 'wb') as f:
        f.write(image_bytes)

    # return jsonify("check_image()")
    return jsonify(check_image())


if __name__ == '__main__':
    app.run(debug=True)
