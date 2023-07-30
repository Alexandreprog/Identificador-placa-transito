import os
import re
import random

"""
    Change the label of each class, where each annotation will be labeled in the order they appear in 
    the "subpath" list; that is, subpaths[0] will be assigned the label 0, subpaths[1] will be assigned 
    the label 1, and so on.

    Ensuring that there will be consistency in the value of the labels of the classes used, so that 2 or 
    more annotations have the same label.

    Parameters: 
        root_path: path to project folder
"""
def changeLabel(root_path):
    # annotation of each class
    subpaths = ['circle_annotation', 'octagon_annotation', 'rectangle_annotation', 'rhombus_annotation', 
                'triangle_annotation']

    for index, path in enumerate(subpaths):
        os.chdir(os.path.join(root_path, f'dataset\\{path}'))

        files = os.listdir()

        for file in files:
            content = ''
            with open(file, 'r') as f:
                content = f.read()

                content = re.sub(r'^\d', str(index), content)
            
            with open(file, 'w') as f:
                f.write(content)

"""
    Produces a file with the name of the class that contains all the paths to all the image 
    annotations of that class

    Parameters: 
        root_path: path to project folder
"""
def annotation_path_list(root_path):
    # annotation of each class
    subpaths = ['circle_annotation', 'octagon_annotation', 'rectangle_annotation', 'rhombus_annotation', 
                'triangle_annotation']

    for index, path in enumerate(subpaths):
        os.chdir(os.path.join(root_path, f'dataset\\{path}'))

        files = os.listdir()

        with open(os.path.join(root_path, f'dataset\\{path}.txt'), 'w') as f:
            for file in files:
                f.write(os.path.abspath(file) + '\n')

"""
    Produces a training and test file that contains all annotation paths for randomly selected 
    images.

    Parameters: 
        root_path: path to project folder
"""
def generate_train_test_files(root_path):
    # annotation of each class
    subpaths = ['circle_annotation', 'octagon_annotation', 'rectangle_annotation', 'rhombus_annotation', 
                'triangle_annotation']

    for path in subpaths:
        indexes = []

        with open(os.path.join(root_path, f'dataset\\{path}.txt'), 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]

            """
                The for loop below randomly chooses 700 images from each class, totaling 3500 images, which 
                corresponds to the size of the training data.
            """
            for i in range(700):
                delete = random.randint(0, len(lines) - 1)
                while delete in indexes:
                    delete = random.randint(0, len(lines) - 1)
                
                indexes.append(delete)

            with open(os.path.join(root_path, f'dataset\\train.txt'), 'a') as fo:
                fo.writelines(line + '\n'for idx, line in enumerate(lines) if idx in indexes)
            
            with open(os.path.join(root_path, f'dataset\\test.txt'), 'a') as fo:
                fo.writelines(line + '\n' for idx, line in enumerate(lines) if idx not in indexes)

"""
    The function below gets the image paths from the path of their respective annotations.

    Parameters: 
        root_path: path to project folder
"""
def changePath(root_path):
    names = ['train', 'test']

    for name in names:
        with open(os.path.join(root_path, f'dataset\\{name}.txt'), 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]

            with open(os.path.join(root_path, f'dataset\\{name}_t.txt'), 'w') as fo:
                for line in lines:
                    
                    if 'circle_annotation' in line:
                        content = line.replace('circle_annotation', 'circle\\images')

                    elif 'octagon_annotation' in line:
                        content = line.replace('octagon_annotation', 'octagon\\images')

                    elif 'rectangle_annotation' in line:
                        content = line.replace('rectangle_annotation', 'rectangle\\images')

                    elif 'rhombus_annotation' in line:
                        content = line.replace('rhombus_annotation', 'rhombus\\images')

                    elif 'triangle_annotation' in line:
                        content = line.replace('triangle_annotation', 'triangle\\images')
                    
                    content = content.replace('.txt', '.png')

                    fo.write(content + '\n')
    
    os.remove(os.path.join(root_path, f'dataset\\train.txt'))
    os.remove(os.path.join(root_path, f'dataset\\test.txt'))

    os.rename(os.path.join(root_path, f'dataset\\train_t.txt'), os.path.join(root_path, f'dataset\\train.txt'))
    os.rename(os.path.join(root_path, f'dataset\\test_t.txt'), os.path.join(root_path, f'dataset\\test.txt'))

# Calling the functions
changeLabel(os.getcwd())
annotation_path_list(os.getcwd())
generate_train_test_files(os.getcwd())
changePath(os.getcwd())