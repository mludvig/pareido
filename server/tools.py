#!/usr/bin/env python3

import json
from io import BytesIO
import exif
from PIL import Image, ImageDraw, ImageFont

def output_image(image, detections, embed_exif=True):
    image_new = draw_detections(image, detections)
    image_buf = BytesIO()
    image_new.save(image_buf, 'JPEG', quality=80)
    image_buf.seek(0)

    if embed_exif:
        image_exif = exif.Image(image_buf)
        image_exif['user_comment'] = dump_json(detections, mode='compact', decimals=2)
        image_exif['software'] = 'Image Service'
        image_buf = BytesIO()
        image_buf.write(image_exif.get_file())
        image_buf.seek(0)

    return image_buf

def draw_detections(image, detections):
    line_width = 2
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("FreeMono.ttf", 15)
    for d in detections:
        rect = (d['x1'], d['y1'], d['x2'], d['y2'])
        draw.rectangle(rect, outline='lightgreen', width=line_width)

        text = f"{d['score']:.1f}%"
        text_size = font.getsize(text)
        if d['y1'] < text_size[1]:
            # place label above detection
            text_rect = (d['x1']+line_width, d['y1']+line_width, d['x1']+text_size[0]+line_width, d['y1']+text_size[1]+line_width)
        else:
            # place label inside detection
            text_rect = (d['x1'], d['y1']-1-text_size[1], d['x1']+text_size[0], d['y1']-1)
        draw.rectangle(text_rect, outline='yellow', fill='yellow')
        draw.text(text_rect[:2], text, fill='black', font=font)
    return image

def dump_json(data, mode='pretty', decimals=None):
    if mode == 'pretty':
        dumps_kwargs = {
            'indent': 2,
        }
    else:
        dumps_kwargs = {
            'indent': None,
            'separators': (',', ':'),
        }
    out = json.dumps(data, **dumps_kwargs)
    if decimals is not None:
        # Round up floats to 'decimals' places to save space
        # https://stackoverflow.com/a/29066406/940259
        out = json.dumps(json.loads(out, parse_float=lambda x: round(float(x), decimals)), **dumps_kwargs)
    return out
