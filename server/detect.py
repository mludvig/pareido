#!/usr/bin/env python3

from PIL import Image
from openvino_person_detection_retail import InferenceModel  # import the AI Model
from modelplace_api import Device

model = InferenceModel()        # Load once
model.model_load(Device.cpu)

def detect(image, min_confidence=0, min_area=0):
    image = Image.open(image).convert("RGB")
    results = model.process_sample(image)
    return filter_results(image, results, min_confidence, min_area)

def filter_results(image, results, min_confidence, min_area):
    out = []
    for result in results:
        result = dict(result)
        result["score"] *= 100  # We use 0%-100% score
        if result["score"] < min_confidence:
            print(f"Low score: {result['score']}")
            continue
        image_area = image.size[0]*image.size[1]
        result_area = (result["x2"]-result["x1"]) * (result["y2"]-result["y1"])
        result["area"] = 100*result_area/image_area
        if result["area"] < min_area:
            print(f"Small area: {result['area']}")
            continue
        out.append(result)
    return out
