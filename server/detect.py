#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
from openvino_person_detection_retail import InferenceModel  # import the AI Model
from modelplace_api import Device

model = InferenceModel()        # Load once
model.model_load(Device.cpu)

def detect(image):
    #image = Image.open(image).convert("RGB")
    detections = model.process_sample(image)
    return detections

def filter_detections(image, detections, min_score, min_area):
    out = []
    for detection in detections:
        detection = dict(detection)
        detection["score"] *= 100  # We use 0%-100% score
        if detection["score"] < min_score:
            print(f"Low score: {detection['score']}")
            continue
        image_area = image.size[0]*image.size[1]
        detection_area = (detection["x2"]-detection["x1"]) * (detection["y2"]-detection["y1"])
        detection["area"] = 100*detection_area/image_area
        if detection["area"] < min_area:
            print(f"Small area: {detection['area']}")
            continue
        out.append(detection)
    return out

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
