# ESSE ARQUIVO BUILD TEM QUE BAIXAR O MODELO, PRÉ-PROCESSAR OS DADOS E GERAR O ARQUIVO YAML
from src.downloader import Downloader
from src.preprocess import Preprocessor
from utils.build_utils import allocate_split, create_yaml
from sklearn.model_selection import train_test_split
import os
import argparse


def get_build_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_id", type=str)

    return parser.parse_args()


if __name__ == "__main__":
    downloader = Downloader()
    downloader.run()

    processor = Preprocessor()
    processor.run()

    create_yaml(train_path="images/train",
                val_path="images/val",
                test_path="images/test",
                labels=processor.labels)

    images_train, images_else, labels_train, labels_else = train_test_split(
        processor.images_files, processor.labels_files, test_size=0.3)

    images_val, images_test, labels_val, labels_test = train_test_split(
        images_else, labels_else, test_size=10 / len(images_else))

    allocate_split("train", images_train, labels_train)
    allocate_split("val", images_val, labels_val)
    allocate_split("test", images_test, labels_test)