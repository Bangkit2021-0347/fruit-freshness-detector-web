from flask import Flask, request, render_template
import torch.nn as nn
import torch
import numpy as np
from torchvision import transforms
import cv2
import base64
from net import Net

app = Flask(__name__)
MODEL = None
MODEL_FILE = "model.pt"
TORCH_DEVICE = "cpu"


def get_model():
    """Return ML model"""
    global MODEL
    if not MODEL:
        MODEL = Net()
        MODEL.load_state_dict(
            torch.load(MODEL_FILE, map_location=torch.device(TORCH_DEVICE))
        )

    return MODEL

def freshness_label(freshness_percentage):
    """Give freshness label"""
    if freshness_percentage > 90:
        return "Segar"
    elif freshness_percentage > 65:
        return "Baik"
    elif freshness_percentage > 50:
        return "Cukup Baik"
    elif freshness_percentage > 0:
        return "Tidak Baik"
    else:
        return "Busuk"


def price_text(price):
    """Give price text to be rendered in HTML"""
    if price == 0:
        return "Gratis"

    return str(price)


def get_price(freshness_percentage):
    return int(freshness_percentage/100*10000)


def get_freshness_percentage(cv_image):
    """
    Reference: https://github.com/anshuls235/freshness-detector/blob/4cd289fb05a14d3c710813fca4d8d03987d656e5/main.py#L40
    """
    mean = (0.7369, 0.6360, 0.5318)
    std = (0.3281, 0.3417, 0.3704)
    transformation = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean, std)
    ])
    image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (32, 32))
    image_tensor = transformation(image)
    batch = image_tensor.unsqueeze(0)
    out = get_model()(batch)
    s = nn.Softmax(dim=1)
    result = s(out)
    return int(result[0][0].item()*100)

def imdecode_image(image_file):
    return cv2.imdecode(
        np.frombuffer(image_file.read(), np.uint8),
        cv2.IMREAD_UNCHANGED
    )

def recognize(cv_image):
    freshness_percentage = get_freshness_percentage(cv_image)
    return {
        "freshness_level": freshness_percentage,
        "price": get_price(freshness_percentage)
    }

@app.route('/api/recognize', methods=["POST"])
def api_recognize():
    cv_image = imdecode_image(request.files["image"])
    return recognize(cv_image)


@app.route("/")
def index_page():
    return render_template("index.html")

@app.route("/checkout", methods=["POST"])
def checkout_page():
    cv_image = imdecode_image(request.files["image"])
    recognize_result = recognize(cv_image)
    freshness_percentage = recognize_result["freshness_level"]

    # show submitted image
    image_content = cv2.imencode('.jpg', cv_image)[1].tobytes()
    encoded_image = base64.encodebytes(image_content)
    base64_image = 'data:image/jpg;base64, ' + str(encoded_image, 'utf-8')
    return render_template(
        "checkout.html",
        freshness_percentage=freshness_percentage,
        freshness_label=freshness_label(freshness_percentage),
        base64_image=base64_image,
        price=price_text(recognize_result["price"])
    )
