import yaml
import os
import random


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
        os.replace(f"datasets/labels/{label}", f"datasets/labels/{name}/{label}")
        for label in labels_list
    ]


def stratified_sampling(labels_list, labels, test_ratio, verbose=False):
    random.seed(123)
    
    # num total de cada label
    num_label = [0 for _ in labels]

    # num de cada label em cada img
    num_label_per_img = {file: [0 for _ in labels] for file in labels_list}

    for file in labels_list:
        with open(f"datasets/labels/{file}", "r") as f:
            for line in f:
                label = int(line[0])

                num_label[label] += 1
                num_label_per_img[file][label] += 1

    # numero alvo de samples no conjunto de teste
    target_test_samples_per_label = [n * test_ratio for n in num_label]
    target_train_samples_per_label = [
        num_label[i] - target_test_samples_per_label[i] for i in range(len(labels))
    ]

    # sample pool vai ser dividida nas duas listas
    sample_pool = labels_list
    train_list = []
    test_list = []

    # escolhe uma img da lista levando em conta o alvo de samples
    def weighted_sampling(samples_per_label):

        sample = random.choices(
            sample_pool,
            # peso de cada img é proporcional a
            # quanto a ela tem * quanto precisamos, para cada label
            weights=[
                sum(
                    [
                        num_label_per_img[img][label] * samples_per_label[label]
                        for label in range(len(labels))
                    ]
                )
                for img in sample_pool
            ],
        )[0]

        # deduz a qtd de samples dessa img do alvo
        for label in range(len(labels)):
            samples_per_label[label] -= num_label_per_img[sample][label]

        sample_pool.remove(sample)
        return sample

    # escolhe uma img para cada lista até esvaziar a pool
    while len(sample_pool) > 0:

        # se o alvo do test foi atingido, não escolhe mais nenhuma img pra ele
        if sum(target_test_samples_per_label) > 0:
            test_list.append(
                weighted_sampling(target_test_samples_per_label)
            )

        train_list.append(
            weighted_sampling(target_train_samples_per_label)
        )

    if verbose:
        # imprime proporção das labels no dataset
        print("Dataset label proportion:")
        print(dict(zip(labels, num_label)))

        # imprime qtd de cada label no array train e test
        num_label_train = [0, 0, 0]
        for sample in train_list:
            for label in range(len(labels)):
                num_label_train[label] += num_label_per_img[sample][label]

        num_label_test = [0, 0, 0]
        for sample in test_list:
            for label in range(len(labels)):
                num_label_test[label] += num_label_per_img[sample][label]

        print("Qty of each in label in train list")
        print(num_label_train)
        print("Qty of each in label in test list")
        print(num_label_test)
        print("")

    # pega o nome dos arquivos de img a partir dos nomes dos arquivos de label
    train_list_img = [name.split(".")[0] + ".png" for name in train_list]
    test_list_img = [name.split(".")[0] + ".png" for name in test_list]

    return train_list_img, test_list_img, train_list, test_list


def print_label_distribution(labels_list, labels):
    # num total de cada label
    num_label = [0 for _ in labels]

    for file in labels_list:
        with open(f"datasets/labels/{file}", "r") as f:
            for line in f:
                label = int(line[0])

                num_label[label] += 1

    # imprime proporção das labels no dataset
    print("Dataset label distribution:")
    print(dict(zip(labels, num_label)))
