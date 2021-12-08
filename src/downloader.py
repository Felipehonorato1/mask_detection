import os


class Downloader():
    def __init__(self):
        pass

    def run(self):
        print("Downloading dataset")
        
        if not os.path.isdir("datasets"):
            os.mkdir("datasets")
        
        if not os.path.isdir("datasets/annotations"):
            os.system("gdown --id 1oAyv_U637hOzyFY34F_VWaWEtg8wYMz3")
            os.replace("mask_data.zip", "datasets/mask_data.zip")
            os.system("unzip datasets/face_mask.zip -d datasets/")
            os.remove("datasets/face_mask.zip")
        else:
            print("- Dataset already exists")

        if not os.path.isdir("yolov5"):
            print("Cloning YoloV5 repo")
            os.system("git clone https://github.com/humbertonc/yolov5")
            
        print("Done")
