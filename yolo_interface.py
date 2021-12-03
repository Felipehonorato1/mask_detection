from pathlib import PosixPath
from os import listdir
from yolov5 import detect
import io

no_incorrect = 0
no_without = 0

def capture_log():
    global no_incorrect
    global no_without

    f = open('bot_msg.txt', 'r')
    s = f.read()
    f.close()

    i = s.find('mask_weared_incorrect')
    if i > 0:
        no_incorrect = int(s[i - 2])
    else:
        no_incorrect = 0

    i = s.find('without_mask')
    if i > 0:
        no_without = int(s[i - 2])
    else:
        no_without = 0

    return


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
        save_crop_labels=['mask_weared_incorrect', 'without_mask'],
        save_txt=False,
        source=source,
        update=False,
        view_img=False,
        visualize=False,
        weights=PosixPath("yolov5/runs/train/exp/weights/best.pt"),
    )

    # Run detect.py
    detect.main(opt)


# Checks YOLO output for maskless labels, and if any are found return true and that output
def check_masked():
    buffer_incorrect = no_incorrect
    buffer_without = no_without

    capture_log()

    img_dir = PosixPath('crops')
    imgs = []
    if img_dir.exists():
        for img in listdir(img_dir):
            imgs.append(img)

    if buffer_incorrect != no_incorrect or buffer_without != no_without:
        return True, str(no_incorrect) + ' máscaras vestidas incorretamente. ' + str(no_without) + ' sem máscara.', imgs
    
    return False, '', []

if __name__ == "__main__":
    init_yolo()
