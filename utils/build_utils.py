import yaml
import os


def create_yaml(labels, train_path, val_path, test_path):

    data = dict(
        train=train_path,
        val=val_path,
        test=test_path,
        path="../datasets",
        nc=3,
        names=labels,
    )

    with open("train_config.yaml", "w") as f:
        yaml.dump(data, f, explicit_start=True)

    return


def allocate_split(name, imgs_list, labels_list):
    # CRIA OS DIRETÓRIOS
    os.mkdir(f"datasets/images/{name}")
    os.mkdir(f"datasets/labels/{name}")

    # MOVE AS IMAGENS E OS LABELS
    [
        os.replace(f"datasets/images/{img}", f"datasets/images/{name}/{img}")
        for img in imgs_list
    ]
    [
        os.replace(f"datasets/labels/{label}",
                   f"datasets/labels/{name}/{label}") for label in labels_list
    ]
