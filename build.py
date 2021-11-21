# ESSE ARQUIVO BUILD TEM QUE BAIXAR O MODELO, PRÉ-PROCESSAR OS DADOS E GERAR O ARQUIVO YAML
from src.downloader import Downloader
from src.preprocess import Preprocessor
from utils.build_utils import create_yaml
from sklearn.model_selection import train_test_split
import argparse


def get_build_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_id", type=str)


if __name__ == "__main__":
    downloader = Downloader()
    downloader.run()

    processor = Preprocessor()
    processor.run()

    create_yaml(train_path="images/train", val_path="images/val",
                test_path="images/test", labels=processor.labels)
