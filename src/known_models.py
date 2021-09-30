# fmt: off
known_models = [
    {
        "name": "Person detection",
        "slug": "person",
        "module_name": "openvino_person_detection_retail",
        "url": "https://modelplace.ai/models/17",
    },
    {
        "name": "Person Vehicle Bike",
        "slug": "pvb",
        "module_name": "openvino_person_vehicle_bike_detection_crossroad",
        "url": "https://modelplace.ai/models/19",
    },
    {
        "name": "Pedestrian detection",
        "slug": "pedestrian",
        "module_name": "openvino_pedestrian_detection_adas",
        "url": "https://modelplace.ai/models/18",
    },
    {
        "name": "MobileNet SSD",
        "slug": "mobilenet",
        "module_name": "openvino_mobilenet_ssd",
        "url": "https://modelplace.ai/models/26",
    },
    {
        "name": "CenterNet",
        "slug": "centernet",
        "module_name": "openvino_centernet",
        "url": "https://modelplace.ai/models/3",
    },
    {
        "name": "Face detection",
        "slug": "face",
        "module_name": "openvino_face_detection_retail",
        "url": "https://modelplace.ai/models/16",
    },
    {
        "name": "YOLO v3",
        "slug": "yolov3",
        "module_name": "openvino_yolo_v3",
        "url": "https://modelplace.ai/models/29",
    },
    {
        "name": "Tiny YOLO v3",
        "slug": "tinyyolov3",
        "module_name": "openvino_tiny_yolo_v3",
        "url": "https://modelplace.ai/models/28",
    },
    {
        "name": "Tiny YOLO v4",
        "slug": "tinyyolov4",
        "module_name": "openvino_yolov4_tiny",
        "url": "https://modelplace.ai/models/32",
    },
]
# fmt: on

if __name__ == "__main__":
    for model in known_models:
        print(model["module_name"])
