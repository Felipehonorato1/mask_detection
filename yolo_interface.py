from pathlib import PosixPath
from yolov5 import detect
import io
# from yolov5.utils.general import LOGGER
# import logging


# StringIO with yolo output
# global variable so check_masked has access to it
YOLO_CAPTURE = None

# TODO
# Gets a StringIO stream with LOGGER output
def capture_log():
    capture_string = io.StringIO()
    # capture_handler = logging.StreamHandler(capture_string)
    # capture_handler.setLevel(logging.INFO)
    # LOGGER.addHandler(capture_string)
    return capture_string


# Initializes yolo
def init_yolo(source: str):
    # Simulate detect.py command line arguments
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    if source is None:
        source = "0"

    opt = Namespace(
        agnostic_nms=False,
        augment=False,
        classes=None,
        conf_thres=0.25,
        device="",
        dnn=False,
        exist_ok=False,
        half=False,
        hide_conf=False,
        hide_labels=False,
        imgsz=[640, 640],
        iou_thres=0.45,
        line_thickness=3,
        max_det=1000,
        name="exp",
        nosave=False,
        project=PosixPath("yolov5/runs/detect"),
        save_conf=False,
        save_crop=False,
        save_txt=False,
        source=source,
        update=False,
        view_img=False,
        visualize=False,
        weights=PosixPath("yolov5/yolov5s.pt"),
    )

    # Run detect.py
    detect.main(opt)


def start(source: str):
    # Set YOLO_CAPTURE to LOGGER output
    YOLO_CAPTURE = capture_log()
    # Initialize YOLO
    init_yolo(source)


# Checks YOLO output for maskless labels, and if any are found return true and that output
def check_masked():
    if YOLO_CAPTURE is None:
        return True, "yolo capture not set"

    # TODO deve checar o output do yolo e se houver alguém sem mascara deve
    # retornar verdadeiro + uma string dizendo quantas pessoas sem mascara

    # TODO retornar também uma captura do momento que estava sem máscara

    return True, "test message"


if __name__ == "__main__":
    init_yolo()
