#!/usr/bin/env python3

import os
import json
from io import BytesIO
import exif
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(__file__)


def resize_image(image, max_size):
    if image.width <= max_size[0] and image.height <= max_size[1]:
        return image

    if image.width/image.height < max_size[0]/max_size[1]:
        # resize by height
        ratio = image.height/max_size[1]
    else:
        # resize by width
        ratio = image.width/max_size[0]
    new_size = (
        int(image.width / ratio),
        int(image.height / ratio)
    )
    image = image.resize(new_size, Image.BICUBIC)
    return image


def output_image(image, detections, embed_exif=False, max_size=(1024, 1024)):
    if max_size:
        det_rel = detections_absolute2relative(image, detections)
        image = resize_image(image, max_size)
        detections = detections_relative2absolute(image, detections)

    image = draw_detections(image, detections)
    image_buf = BytesIO()
    image.save(image_buf, "JPEG", quality=80)
    image_buf.seek(0)

    if embed_exif:
        image_exif = exif.Image(image_buf)
        image_exif["software"] = "Pareido - https://github.com/mludvig/pareido"
        user_comment = dump_json(detections, mode="compact", decimals=2)
        # User comment needs at least 4 chars - otherwise 'exif' crashes
        image_exif["user_comment"] = f"{user_comment:4s}"
        image_buf = BytesIO()
        image_buf.write(image_exif.get_file())
        image_buf.seek(0)

    return image_buf


def draw_detections(image, detections):
    colours = ["lightgreen", "lightblue", "yellow", "pink", "orange" ]
    label_colours = {}

    line_width = 2
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(f"{SCRIPT_DIR}/fonts/FreeMono.ttf", 15)
    for d in detections:
        # Pick a colour
        if d['class_name'] not in label_colours:
            try:
                colour = colours.pop(0)
            except IndexError:
                colour = "white"
            label_colours[d['class_name']] = colour
        else:
            colour = label_colours[d['class_name']]

        # Bounding box
        rect = (d["x1"], d["y1"], d["x2"], d["y2"])
        draw.rectangle(rect, outline=colour, width=line_width)
        # Label + Score
        text = f"{d['class_name']} {d['score']:.1f}%"
        text_size = font.getsize(text)
        if d["y1"] < text_size[1]:
            # place score above detection
            text_rect = (
                d["x1"] + line_width,
                d["y1"] + line_width,
                d["x1"] + text_size[0] + line_width,
                d["y1"] + text_size[1] + line_width,
            )
        else:
            # place label inside detection
            text_rect = (
                d["x1"],
                d["y1"] - 1 - text_size[1],
                d["x1"] + text_size[0],
                d["y1"] - 1,
            )
        draw.rectangle(text_rect, outline=colour, fill=colour)
        draw.text(text_rect[:2], text, fill="black", font=font)

    return image


def dump_json(data, mode="pretty", decimals=None):
    if mode == "pretty":
        dumps_kwargs = {
            "indent": 2,
        }
    else:
        dumps_kwargs = {
            "indent": None,
            "separators": (",", ":"),
        }
    out = json.dumps(data, **dumps_kwargs)
    if decimals is not None:
        # Round up floats to 'decimals' places to save space
        # https://stackoverflow.com/a/29066406/940259
        out = json.dumps(
            json.loads(out, parse_float=lambda x: round(float(x), decimals)),
            **dumps_kwargs,
        )
    return out


def detections_absolute2relative(image, detections):
    out = []
    for detection in detections:
        detection["x1"] /= image.width
        detection["x2"] /= image.width
        detection["y1"] /= image.height
        detection["y2"] /= image.height
        out.append(detection)
    return out


def detections_relative2absolute(image, detections):
    out = []
    for detection in detections:
        detection["x1"] = int(detection["x1"] * image.width)
        detection["x2"] = int(detection["x2"] * image.width)
        detection["y1"] = int(detection["y1"] * image.height)
        detection["y2"] = int(detection["y2"] * image.height)
        out.append(detection)
    return out
