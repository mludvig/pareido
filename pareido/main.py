#!/usr/bin/env python3

import time
import json

from PIL import Image
from flask import Blueprint, request, Response, send_file, render_template, redirect

from .models import detect, filter_detections, models, get_active_models, get_all_models
from .tools import output_image, dump_json

bp = Blueprint("pareido", __name__)


@bp.route("/", methods=["GET"])
def index_get():
    return render_template("index.html", models=get_active_models())


@bp.route("/models", methods=["GET"])
def models_get():
    active_models = get_active_models()
    return Response(json.dumps(active_models, indent=2), mimetype="application/json")


@bp.route("/models/all", methods=["GET"])
def models_all_get():
    all_models = get_all_models()
    return Response(json.dumps(all_models, indent=2), mimetype="application/json")


@bp.route("/detect", methods=["GET"])
def detect_get():
    return redirect("/", code=302)


@bp.route("/detect", methods=["POST"])
def detect_post():
    # Find the parameters either in form data or in query args
    output = request.values.get("output", "json")
    min_confidence = float(request.values.get("min_confidence", 0))
    min_area = float(request.values.get("min_area", 0))
    pretty_output = bool(request.values.get("pretty", ""))
    exif_detections = bool(request.values.get("exif", ""))
    default_model = get_active_models()[0]
    model_slug = request.values.get("model", default_model["slug"])

    if model_slug not in models:
        result = {"error": "Unknown model"}
        return Response(json.dumps(result), status=400, mimetype="application/json")

    results = []
    for _file in request.files:
        try:
            # Open the image in PIL format
            image = Image.open(request.files[_file]).convert("RGB")
        except Exception:
            result = {"error": "Invalid or missing image"}
            return Response(json.dumps(result), status=400, mimetype="application/json")

        # Time the detection
        start_ts = time.time()
        detections = detect(model_slug, image)
        elapsed_ms = (time.time() - start_ts) * 1000
        detections = filter_detections(image, detections, min_confidence, min_area)

        # Draw the results if output == "image"
        if output in ["image", "jpeg", "jpg"]:
            return send_file(
                output_image(image, detections, exif_detections), mimetype="image/jpeg"
            )

        # Else send detections as JSON
        results.append(
            {
                "filename": request.files[_file].filename,
                "elapsed_ms": elapsed_ms,
                "model": model_slug,
                "detections": detections,
            }
        )

    dump_mode = "pretty" if pretty_output else "compact"
    return Response(dump_json(results, dump_mode), mimetype="application/json")
