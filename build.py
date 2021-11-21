# ESSE ARQUIVO BUILD TEM QUE BAIXAR O MODELO, PRÉ-PROCESSAR OS DADOS E GERAR O ARQUIVO YAML
from src.preprocess import Preprocessor
import argparse


def get_build_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_id", type=str)


if __name__ == "__main__":
    preprocessor = Preprocessor()
    preprocessor.run()
