#!/usr/bin/env python3

from openvino_person_detection_retail import InferenceModel  # import the AI Model
from modelplace_api import Device

model = InferenceModel()  # Load once
model.model_load(Device.cpu)


def detect(image):
    detections = model.process_sample(image)
    return detections


def filter_detections(image, detections, min_score, min_area):
    out = []
    for detection in detections:
        detection = dict(detection)
        detection["score"] *= 100  # We use 0%-100% score
        if detection["score"] < min_score:
            # print(f"Low score: {detection['score']}")
            continue
        image_area = image.size[0] * image.size[1]
        detection_area = (detection["x2"] - detection["x1"]) * (
            detection["y2"] - detection["y1"]
        )
        detection["area"] = 100 * detection_area / image_area
        if detection["area"] < min_area:
            # print(f"Small area: {detection['area']}")
            continue
        out.append(detection)
    return out
