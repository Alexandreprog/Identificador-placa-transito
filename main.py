from PIL import Image
import numpy as np
import os
import data_argumentation

folders = ['circle', 'octagon', 'rectangle', 'rhombus', 'triangle']
os.chdir(os.path.join(os.getcwd(), "dataset"))

for folder in folders:
    os.chdir(os.path.join(os.getcwd(),f'{folder}'))
    path = os.getcwd()

    files = os.listdir(path)

    for file in files:
        image = Image.open(path + "\\" + str(file))
        image = image.convert("RGB")

        new_image = data_argumentation.grey_scale(image)
        new_image = Image.fromarray(new_image)
        new_image.save(path + "\\" + str(file).replace(".png", f"_0.png"))

        new_image = data_argumentation.flip(image, horizontal=True)
        new_image = Image.fromarray(new_image)
        new_image.save(path + "\\" + str(file).replace(".png", f"_1.png"))

        new_image = data_argumentation.rotation(45, image, image.height, image.width)
        new_image = Image.fromarray(new_image.astype(np.uint8))
        new_image.save(path + "\\" + str(file).replace(".png", f"_2.png"))

        new_image = data_argumentation.negative(image)
        new_image = Image.fromarray(new_image)
        new_image.save(path + "\\" + str(file).replace(".png", f"_3.png"))
    
    os.chdir("..")