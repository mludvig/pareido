#!/usr/bin/env python3

import time
import json
from io import BytesIO

from PIL import Image
from flask import Flask, request, Response, send_file, render_template, redirect

from detect import detect, filter_detections, draw_detections

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
    min_confidence = float(request.values.get('min_confidence', 0))
    min_area = float(request.values.get('min_area', 0))
    output = request.values.get('output', 'json')
    pretty_output = request.values.get('pretty_output', '')

    results = []
    for _file in request.files:
        try:
            # Open the image in PIL format
            image = Image.open(request.files[_file]).convert("RGB")
        except Exception as e:
            result = {"error": "Invalid or missing image"}
            return Response(json.dumps(result), status=400, mimetype="application/json")

        # Time the detection
        start_ts = time.time()
        detections = detect(image)
        elapsed_sec = time.time() - start_ts
        detections = filter_detections(image, detections, min_confidence, min_area)

        # Draw the results if output == "image"
        if output == "image":
            image_new = draw_detections(image, detections)
            image_buf = BytesIO()
            image_new.save(image_buf, 'JPEG', quality=80)
            image_buf.seek(0)
            return send_file(image_buf, mimetype="image/jpeg")

        # Else send detections as JSON
        results.append({
            "filename": request.files[_file].filename,
            "elapsed_sec": elapsed_sec,
            "detections": detections,
        })

    dumps_kwargs = {}
    if pretty_output:
        dumps_kwargs = {
            'indent': 2,
        }
    else:
        dumps_kwargs = {
            'indent': None,
            'separators': (',', ':'),
        }
    return Response(json.dumps(results, **dumps_kwargs), mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000")
