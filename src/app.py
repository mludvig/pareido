#!/usr/bin/env python3

import time
import json

from PIL import Image
from flask import Flask, request, Response, send_file, render_template, redirect

from .detect import detect, filter_detections
from .tools import output_image, dump_json

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index_get():
    return render_template("index.html")


@app.route("/detect", methods=["GET"])
def detect_get():
    return redirect("/", code=302)


@app.route("/detect", methods=["POST"])
def detect_post():
    # Find the parameters either in form data or in query args
    output = request.values.get("output", "json")
    min_confidence = float(request.values.get("min_confidence", 0))
    min_area = float(request.values.get("min_area", 0))
    pretty_output = bool(request.values.get("pretty_output", ""))
    exif_detections = bool(request.values.get("exif", ""))

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
        detections = detect(image)
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
                "detections": detections,
            }
        )

    dump_mode = "pretty" if pretty_output else "compact"
    return Response(dump_json(results, dump_mode), mimetype="application/json")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000")
