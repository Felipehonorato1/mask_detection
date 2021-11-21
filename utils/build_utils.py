import yaml


def create_yaml(labels, train_path, val_path, test_path):

    data = dict(
        train=train_path,
        val=val_path,
        test=test_path,
        path="datasets",
        nc=3,
        names=labels,
    )

    with open("train_config.yaml", "w") as f:
        yaml.dump(data, f, explicit_start=True)

    return
