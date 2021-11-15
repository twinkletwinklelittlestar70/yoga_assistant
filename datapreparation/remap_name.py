
import os
import base64
FILE_DIR = "../../yoga_data/label_data/dataset"    #label好的数据目录
ORIGIN_DIR = "../../yoga_data/datasets/kaggle_data"

renameFile = "remap_2.txt"
name_map_file = open(renameFile,"w")

all_data_map = {} # key value 形式存储base64，会不会内存爆炸...？
support_classes = [] # 支持的class

all_classes = os.listdir(FILE_DIR)
if '.DS_Store' in all_classes: # 忽略系统文件
  all_classes.remove('.DS_Store')

# 遍历posture class
for cindex, posture in enumerate(all_classes):
  if posture == '.DS_Store': # 忽略unix下系统文件
    continue
  print('Handleing posture ', posture)
  support_classes.append(posture)

  all_groups = os.listdir(os.path.join(FILE_DIR, posture))
  for gindex, group in enumerate(all_groups):
    if group == '.DS_Store': # 忽略unix下系统文件
      continue

    images = os.listdir(os.path.join(FILE_DIR, posture, group))
    for iindex, img in enumerate(images):
      if img == '.DS_Store': # 忽略unix下系统文件
        continue
      
      img_path = os.path.join(FILE_DIR, posture, group, img)
      f = open(img_path,'rb')
      img_base64 = base64.b64encode(f.read())
      f.close()
      all_data_map[img_path] = img_base64

# 根据需要的类遍历原数据
for img_new_path in all_data_map:
    pos_name = img_new_path.split('/')[-3]
    print('handleing img', img_new_path)
    new_img_base64 = all_data_map[img_new_path] # 新图片的base64字符串
    
    # 遍历类下面，寻找base64一样的图片
    all_images = os.listdir(os.path.join(ORIGIN_DIR, pos_name))
    for iindex, img in enumerate(all_images):
      old_img_path = os.path.join(ORIGIN_DIR, pos_name, img)
      f = open(old_img_path, 'rb')
      old_img_base64 = base64.b64encode(f.read())
      f.close()
      if old_img_base64 == new_img_base64:
        all_data_map[img_new_path] = old_img_path
        break

# 把对象写出来
for img_new_path in all_data_map:
  name_map_file.writelines(img_new_path + '   ' + all_data_map[img_new_path] + '\n') # 写出来确认一下文件数量


name_map_file.close()

