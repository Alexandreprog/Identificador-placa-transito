from PIL import Image
import math
import numpy as np

def grey_scale(image):
  assert isinstance(image, Image.Image)

  image_arr = np.array(image)
  image_arr[:,:,1] = image_arr[:,:,0]
  image_arr[:,:,2] = image_arr[:,:,0]

  return image_arr

def flip(image, **kwargs):
  assert isinstance(image, Image.Image)

  image_arr = np.array(image)

  if 'horizontal' in kwargs and kwargs['horizontal']:
    image_arr = image_arr[:,::-1]
  
  if 'vertical' in kwargs and kwargs['vertical']:
    image_arr = image_arr[::-1,:]

  return image_arr

def end_position_point(angle, i,j, move_i0, move_j0):
  end_i = int((i)*math.cos(math.radians(angle)) - (j)*math.sin(math.radians(angle))) + move_i0
  end_j = int((i)*math.sin(math.radians(angle)) + (j)*math.cos(math.radians(angle))) + move_j0

  return (end_i, end_j)

def move_points(angle, img_height, img_width):
  i = []
  j = []

  end_i, end_j = end_position_point(angle, 0, img_width - 1, 0, 0)

  i.append(end_i)
  j.append(end_j)

  end_i, end_j = end_position_point(angle, img_height - 1, 0, 0, 0)

  i.append(end_i)
  j.append(end_j)  

  end_i, end_j = end_position_point(angle, img_height - 1, img_width - 1, 0, 0)

  i.append(end_i)
  j.append(end_j)  

  i = list(filter(lambda x: x < 0, i))
  j = list(filter(lambda x: x < 0, j))

  i = list(map(lambda x: abs(x), i))
  j = list(map(lambda x: abs(x), j))

  if len(i) == 0:
    i.append(0)

  if len(j) == 0:
    j.append(0)

  return (max(i), max(j))

def rotation(angle, image, height, width):
  image_arr = np.array(image)
  move_i0, move_j0 = move_points(angle, height, width)
  
  max_dimension = int(np.sqrt(width**2 + height**2))
  rotated_image = np.full((max_dimension, max_dimension, 3), 255)

  for i in range(height):
    for j in range(width):
      end_i, end_j = end_position_point(angle, i, j, move_i0, move_j0)

      rotated_image[end_i][end_j] = image_arr[i][j]
  
  return rotated_image

def negative(image):
  width, height = image.size
  image_arr = np.array(image)

  for i in range(height):
    for j in range(width):
      for k in range(3):
        image_arr[i][j][k] = max(0,255 - image_arr[i][j][k])
  
  return image_arr