def get_yolo(img_width, img_height, x_min, y_min, x_max, y_max):
    x_center = (x_max + x_min) / (2 * img_width)
    y_center = (y_max + y_min) / (2 * img_height)
    width = (x_max - x_min) / img_width
    height = (y_max - y_min) / img_height
    return x_center, y_center, width, height
