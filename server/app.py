#!/usr/bin/env python3

import hashlib
import json

from flask import Flask, request, Response

from detect import detect

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return """
    <!doctype html>
    <html>
    <head>
    <title>Upload new image</title>
    </head>
    <body>
    <h1>Upload new image</h1>
    <form action="/image" method="post" enctype="multipart/form-data">
      Min confidence: <input type="text" name="min_confidence" value="50" size="5"><br/>
      Min area: <input type="text" name="min_area" value="5" size="5"><br/>
      Image: <input type="file" name="image"><br/>
      <input type="submit" value="Upload">
    </form>
    """

@app.route("/image", methods=["POST"])
def image():
    # Test with: 'curl -XPOST -F image=@path/to/image.jpg http://...'
    #print(f"{request.headers=!s}")
    print(f"{request.form=!s}")
    if 'image' not in request.files:
        return json.dumps({"error": "'image' not supplied"}), 400
    image = request.files['image']
    min_confidence = int(request.form.get('min_confidence', 0))
    min_area = int(request.form.get('min_area', 0))
    result = detect(image, min_confidence, min_area)
    return Response(json.dumps({
        "filename": image.filename,
        "result": result,
    }, default=lambda o: o.__dict__, indent=2), mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
