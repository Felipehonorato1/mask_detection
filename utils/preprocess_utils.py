from pathlib import Path
import os


def get_yolo(img_width, img_height, x_min, y_min, x_max, y_max):

    x_center = (x_max + x_min) / (2 * img_width)
    y_center = (y_max + y_min) / (2 * img_height)

    width = (x_max - x_min) / img_width
    height = (y_max - y_min) / img_height

    return x_center, y_center, width, height


def resize_imgs(dirpath, verbose=True):
    for path in Path(dirpath).glob("**/*"):
        if path.suffix in [".png", ".jpg", ".jpeg"]:
            if verbose:
                print(f"Resizing {str(path)}")
            os.system(f"convert {str(path)} -resize 640x640 {str(path)}")
