# fmt: off
known_models = [
    ## Person detection
    {
        "name": "Person Vehicle Bike",
        "slug": "pvb",
        "module_name": "openvino_person_vehicle_bike_detection_crossroad",
        "url": "https://modelplace.ai/models/19",
    },
    {
        "name": "Person detection",
        "slug": "person",
        "module_name": "openvino_person_detection_retail",
        "url": "https://modelplace.ai/models/17",
    },
    {
        "name": "Pedestrian detection",
        "slug": "pedestrian",
        "module_name": "openvino_pedestrian_detection_adas",
        "url": "https://modelplace.ai/models/18",
    },
    ## Face detection
    {
        "name": "Face detection",
        "slug": "face",
        "module_name": "openvino_face_detection_retail",
        "url": "https://modelplace.ai/models/16",
    },
    {
        "name": "Face Detector (Adas)",
        "slug": "faceadas",
        "module_name": "openvino_face_detection_adas",
        "url": "https://modelplace.ai/models/13",
    },
    ## Vehicle detection
    {
        "name": "Vehicle Detector (Adas)",
        "slug": "vehicle",
        "module_name": "openvino_vehicle_detection_adas",
        "url": "https://modelplace.ai/models/20",
    },
    {
        "name": "Vehicle License Detector",
        "slug": "vehiclelicense",
        "module_name": "openvino_vehicle_license_plate_detection_barrier",
        "url": "https://modelplace.ai/models/22",
    },
    ## General object detection
    {
        "name": "Faster R-CNN ResNet-50",
        "slug": "fastercnn",
        "module_name": "pytorch_fastercnn",
        "url": "https://modelplace.ai/models/2",
        "note": "pip3 install pytorch_fastercnn/torch_stable.html",
    },
    {
        "name": "MobileNet SSD",
        "slug": "mobilenetssd",
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
    #{
    #    # Doesn't work with OpenVINO 2021.4
    #    "name": "Tiny YOLO v4",
    #    "slug": "tinyyolov4",
    #    "module_name": "openvino_yolov4_tiny",
    #    "url": "https://modelplace.ai/models/32",
    #},
]
# fmt: on

if __name__ == "__main__":
    for model in known_models:
        print(model["module_name"])
