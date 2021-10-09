#!/usr/bin/env python3

import os
import warnings
import importlib
from loguru import logger
from modelplace_api import Device

from .known_models import known_models

models = {}


def load_models():
    only_models = exclude_models = []
    if os.getenv("PAREIDO_MODELS"):
        only_models = os.getenv("PAREIDO_MODELS").split(",")
    if os.getenv("PAREIDO_MODELS_EXCLUDE"):
        exclude_models = os.getenv("PAREIDO_MODELS_EXCLUDE").split(",")

    for model in known_models:
        if only_models and not model["slug"] in only_models:
            logger.warning(
                f"Excluded model: {model['name']} [{model['slug']} is not in $PAREIDO_MODELS]"
            )
            continue
        if model["slug"] in exclude_models:
            logger.warning(
                f"Excluded model: {model['name']} [{model['slug']} is in $PAREIDO_MODELS_EXCLUDE]"
            )
            continue
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                _module = importlib.import_module(model["module_name"])
            model["inference"] = _module.InferenceModel()
            model["inference"].model_load(Device.cpu)
            models[model["slug"]] = model
            logger.info(f"Loaded model: {model['name']} [{model['slug']}]")
        except ModuleNotFoundError as e:
            logger.warning(
                f"Ignored model: {model['name']} [{model['slug']}] - module '{e.name}' not found"
            )


def get_active_models():
    return [
        {
            "slug": models[model_slug]["slug"],
            "name": models[model_slug]["name"],
            "url": models[model_slug]["url"],
            "active": True,
        }
        for model_slug in models.keys()
    ]


def get_all_models():
    all_models = []
    for model in known_models:
        all_models.append(
            {
                "slug": model["slug"],
                "name": model["name"],
                "url": model["url"],
                "active": model["slug"] in models,
            }
        )
    return all_models


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
