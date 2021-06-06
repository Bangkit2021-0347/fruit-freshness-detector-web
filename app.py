from flask import Flask, request, render_template
import torch.nn as nn
import torch
import numpy as np
from torchvision import transforms
import cv2
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


def get_price(freshness_percentage):
    return int(freshness_percentage/100*10000)


def get_freshness_percentage(image):
    mean = (0.7369, 0.6360, 0.5318)
    std = (0.3281, 0.3417, 0.3704)
    transformation = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean, std)
    ])
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (32, 32))
    image_tensor = transformation(img)
    batch = image_tensor.unsqueeze(0)
    out = get_model()(batch)
    s = nn.Softmax(dim=1)
    result = s(out)
    return int(result[0][0].item()*100)


@app.route('/api/recognize', methods=["POST"])
def api_recognize():
    image_file = request.files["image"]
    image = cv2.imdecode(
        np.frombuffer(image_file.read(), np.uint8),
        cv2.IMREAD_UNCHANGED
    )
    freshness_percentage = get_freshness_percentage(image)
    price = get_price(freshness_percentage)
    return {
        "freshness_level": freshness_percentage,
        "price": price
    }
