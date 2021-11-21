from utils.preprocess_utils import get_yolo
import xml.etree.ElementTree as ET
import os


class Preprocessor():
    def __init__(self):
        self.labels = ['with_mask', 'mask_weared_incorrect', 'without_mask']

        print("Starting preprocessor")
        # percorre pelo annotations

    def run(self):
        print("Starting conversion")
        # cria um diretorio para as anotacoes ja ok
        if not os.path.exists("labels"):
            os.mkdir("labels")

        for element in os.listdir("annotations/"):

            label_filename = element.split(sep=".")[0] + ".txt"
            tree = ET.parse(f'annotations/{element}')

            with open(f"labels/{label_filename}", 'w') as f:

                img_width = int(tree.find("size").findtext("width"))
                img_height = int(tree.find("size").findtext("width"))

                for obj in tree.findall('object'):
                    x_min = int(obj.find('bndbox').findtext('xmin'))
                    y_min = int(obj.find('bndbox').findtext('ymin'))
                    x_max = int(obj.find('bndbox').findtext('xmax'))
                    y_max = int(obj.find('bndbox').findtext('ymax'))

                    yolo_format = get_yolo(
                        img_width, img_height, x_min, y_min, x_max, y_max)

                    f.write(str(self.labels.index(obj.findtext('name'))) +
                            ' ' + ' '.join(map(str, yolo_format)) + '\n')
