import cv2
import os


def main():
    f = open("wrong_imgs.txt", 'w')

    for img in os.listdir("imgs"):

        cv2.imshow("img", cv2.imread(f"imgs/{img}"))
        k = cv2.waitKey(0)

        if k == 101:
            f.write(img + '\n')

        if k == 27:
            quit()

    f.close()


if __name__ == '__main__':
    main()