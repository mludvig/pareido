#!/usr/bin/env python3

import importlib
from loguru import logger
from modelplace_api import Device

from .known_models import known_models

models = {}

for model in known_models:
    try:
        _module = importlib.import_module(model["module_name"])
        model["inference"] = _module.InferenceModel()
        model["inference"].model_load(Device.cpu)
        models[model["slug"]] = model
        logger.info(f"Loaded model: {model['name']}")
    except ModuleNotFoundError as e:
        logger.warning(f"Ignoring model: {model['name']} [module '{e.name}' not found]")


def detect(model_slug, image):
    detections = models[model_slug]["inference"].process_sample(image)
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
