from utils.preprocess_utils import get_yolo
import xml.etree.ElementTree as ET
import os


class Preprocessor():
    def __init__(self):
        self.labels = ['with_mask', 'mask_weared_incorrect', 'without_mask']
        self.labels_files = None
        self.images_files = None

        print("Starting preprocessor")
        # percorre pelo annotations

    def run(self):
        print("Starting conversion")
        
        # cria um diretorio para as anotacoes ja ok
        if not os.path.exists("datasets/labels"):
            os.mkdir("datasets/labels")

        # confere se o diretorio das labels ja tem coisa pra evitar label duplicada
        if not os.listdir("datasets/labels"):

            # converte as annotations pra arquivos txt com o formato do yolo
            for element in os.listdir("datasets/annotations/"):

                label_filename = element.split(sep=".")[0] + ".txt"
                tree = ET.parse(f'datasets/annotations/{element}')

                with open(f"datasets/labels/{label_filename}", 'w') as f:

                    img_width = int(tree.find("size").findtext("width"))
                    img_height = int(tree.find("size").findtext("width"))

                    for obj in tree.findall('object'):
                        x_min = int(obj.find('bndbox').findtext('xmin'))
                        y_min = int(obj.find('bndbox').findtext('ymin'))
                        x_max = int(obj.find('bndbox').findtext('xmax'))
                        y_max = int(obj.find('bndbox').findtext('ymax'))

                        yolo_format = get_yolo(img_width, img_height, x_min, y_min,
                                            x_max, y_max)

                        f.write(
                            str(self.labels.index(obj.findtext('name'))) + ' ' +
                            ' '.join(map(str, yolo_format)) + '\n')

        # desfaz estratificação caso já tenha sido feita
        for name in ["labels", "images"]:
            for elmt in os.listdir(f"datasets/{name}/"):
                if os.path.isdir(f"datasets/{name}/{elmt}"):
                    [
                        os.replace(
                            f"datasets/{name}/{elmt}/{deep_elmt}",
                            f"datasets/{name}/{deep_elmt}")
                            for deep_elmt in os.listdir(f"datasets/{name}/{elmt}")
                    ]
                    os.rmdir(f"datasets/{name}/{elmt}")

        self.labels_files = [elmt for elmt in os.listdir("datasets/labels/")]
        self.labels_files.sort()

        self.images_files = [elmt for elmt in os.listdir("datasets/images/")]
        self.images_files.sort()